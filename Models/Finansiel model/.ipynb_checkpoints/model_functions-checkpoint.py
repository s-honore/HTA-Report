import numpy as np
import numpy_financial as npf
import pandas as pd
from scipy.stats import weibull_min, uniform
import matplotlib.pyplot as plt
import seaborn as sns


def safe_divide(a, b, epsilon=1e-10):
    return np.divide(a, b, out=np.zeros_like(a), where=abs(b)>epsilon)

def safe_roi(gain, cost):
    if cost == 0:
        return np.inf if gain > 0 else -np.inf if gain < 0 else np.nan
    return (gain / cost - 1) * 100
    
def triangular_distribution(minimum, mode, maximum):
    """
    Genererer en værdi fra en triangulær fordeling.
    
    Argumenter:
    minimum (float): Mindste værdi i fordelingen
    mode (float): Mest sandsynlige værdi (toppunktet i trekanten)
    maximum (float): Største værdi i fordelingen
    
    Returnerer:
    float: En tilfældig værdi fra den triangulære fordeling
    """
    u = np.random.uniform(0, 1)
    if u < (mode - minimum) / (maximum - minimum):
        return minimum + np.sqrt(u * (maximum - minimum) * (mode - minimum))
    else:
        return maximum - np.sqrt((1 - u) * (maximum - minimum) * (maximum - mode))

def lowe_syndrom_fremskrivning(befolkningsdata, regioner, prævalens, maks_levetid, form, skala):
    """
    Fremskriver Lowe Syndrom-populationen over tid for flere regioner.

    Argumenter:
    befolkningsdata (pd.DataFrame): Befolkningsdata for alle regioner.
    regioner (list): Liste over regionsnavne der skal fremskrives.
    prævalens (float): Prævalens af Lowe Syndrom.
    maks_levetid (int): Maksimal levetid for Lowe Syndrom-patienter.
    form (float): Formparameter for Weibull-fordeling.
    skala (float): Skalaparameter for Weibull-fordeling.

    Returnerer:
    dict: Fremskrevne Lowe Syndrom-populationsdata for hver region.
    """
    lowe_syndrom_data = {}
    for region in regioner:
        region_data = befolkningsdata[befolkningsdata['region'] == region]
        
        total_befolkning_2023 = region_data[region_data['Time'] == 2023]['Value'].sum()
        lowe_syndrom_2023 = total_befolkning_2023 * prævalens
        
        aldersinterval = np.arange(0, maks_levetid + 1)
        aldersfordeling = weibull_min.pdf(aldersinterval, form, loc=0, scale=skala)
        aldersfordeling /= aldersfordeling.sum()
        
        lowe_syndrom_aldersfordeling_2023 = np.round(lowe_syndrom_2023 * aldersfordeling)
        
        lowe_syndrom_id_2023 = []
        nuværende_id = 0
        for alder, antal in enumerate(lowe_syndrom_aldersfordeling_2023):
            for _ in range(int(antal)):
                lowe_syndrom_id_2023.append((nuværende_id, 2023, alder))
                nuværende_id += 1
        
        lowe_syndrom_data[region] = [lowe_syndrom_id_2023]
        
        for år in range(2024, 2041):
            forrige_års_data = lowe_syndrom_data[region][-1]
            nuværende_år_befolkning = region_data.loc[(region_data['Time'] == år) & (region_data["Age"] == "0")].Value.sum()
            
            nye_tilfælde = nuværende_år_befolkning * prævalens
            
            nuværende_års_data = []
            for id, forrige_år, alder in forrige_års_data:
                if alder < maks_levetid:
                    nuværende_års_data.append((id, år, alder + 1))
            
            nye_id = range(nuværende_id, nuværende_id + int(nye_tilfælde))
            nye_tilfælde_data = [(id, år, 0) for id in nye_id]
            nuværende_års_data.extend(nye_tilfælde_data)
            
            nuværende_id += int(nye_tilfælde)
            
            lowe_syndrom_data[region].append(nuværende_års_data)
    
    return lowe_syndrom_data

def generer_adoptionsrate(år, maks_adoption, forsinkelse, hastighed):
    """
    Genererer en S-formet adoptionsrate kurve.

    Argumenter:
    år (int): Antal år at generere for
    maks_adoption (float): Maksimal adoptionsrate (mellem 0 og 1)
    forsinkelse (float): Forsinkelse i år før adoptionen begynder at stige hurtigt
    hastighed (float): Hastighed af adoptionen

    Returnerer:
    list: Årlige adoptionsrater
    """
    x = np.linspace(0, år-1, år)
    y = maks_adoption / (1 + np.exp(-hastighed * (x - forsinkelse)))
    return y.tolist()

def juster_adoption_for_alder(base_adoption, alder):
    """
    Justerer adoptionsraten baseret på patientens alder.

    Argumenter:
    base_adoption (float): Base adoptionsrate
    alder (int): Patientens alder

    Returnerer:
    float: Justeret adoptionsrate
    """
    if alder <= 5:
        return base_adoption * 1.2  # Højere adoption for yngre patienter
    elif alder <= 18:
        return base_adoption * 1.1
    else:
        return base_adoption * 0.9  # Lavere adoption for ældre patienter

def simuler_fase(succes_sandsynlighed, omkostningsinterval, tidsinterval):
    """
    Simulerer en enkelt fase af lægemiddeludviklingen.

    Argumenter:
    succes_sandsynlighed (float): Sandsynlighed for succes i denne fase.
    omkostningsinterval (tuple): Interval af mulige omkostninger (min, maks).
    tidsinterval (tuple): Interval af mulige varigheder (min, maks).

    Returnerer:
    tuple: Succes (bool), omkostning (float) og tid (float) for fasen.
    """
    succes = np.random.random() < succes_sandsynlighed
    omkostning = np.random.uniform(*omkostningsinterval)
    tid = np.random.uniform(*tidsinterval)
    return succes, omkostning, tid

def simuler_kommercialisering(markedsstørrelse_us, markedsstørrelse_eu, markedspenetration, pris, produktionsomkostning, adoptionsparametre, år, aldersdistribution):
    """
    Simulerer kommercialiseringsfasen af lægemidlet med en mere realistisk adoptionsmodel.

    Argumenter:
    markedsstørrelse_us (int): Total adresserbar markedsstørrelse i USA.
    markedsstørrelse_eu (int): Total adresserbar markedsstørrelse i EU.
    markedspenetration (float): Forventet markedspenetration.
    pris (float): Pris pr. behandling.
    produktionsomkostning (float): Omkostning til at producere hver behandling.
    adoptionsparametre (dict): Parametre for adoptionsraten for USA og EU.
    år (int): Antal år der skal simuleres.
    aldersdistribution (list): Liste over antal patienter i hver aldersgruppe.

    Returnerer:
    tuple: Lister over årlig omsætning og omkostninger.
    """
    omsætning_us = generer_adoptionsrate(år, 
                                         adoptionsparametre['us']['maks_adoption'], 
                                         adoptionsparametre['us']['forsinkelse'], 
                                         adoptionsparametre['us']['hastighed'])
    omsætning_eu = generer_adoptionsrate(år, 
                                         adoptionsparametre['eu']['maks_adoption'], 
                                         adoptionsparametre['eu']['forsinkelse'], 
                                         adoptionsparametre['eu']['hastighed'])
    
    omsætning = []
    omkostninger = []
    patienter = []
    behandlede_patienter = []
    
    for år_index in range(år):
        årlige_patienter_us = 0
        årlige_patienter_eu = 0
        total_patienter = sum(aldersdistribution)
        
        årlige_patienter_us = total_patienter * markedspenetration * omsætning_us[år_index] * (markedsstørrelse_us / (markedsstørrelse_us + markedsstørrelse_eu))
        årlige_patienter_eu = total_patienter * markedspenetration * omsætning_eu[år_index] * (markedsstørrelse_eu / (markedsstørrelse_us + markedsstørrelse_eu))
        
        årlig_omsætning = (årlige_patienter_us + årlige_patienter_eu) * pris
        årlig_omkostning = (årlige_patienter_us + årlige_patienter_eu) * produktionsomkostning
        
        omsætning.append(årlig_omsætning)
        omkostninger.append(årlig_omkostning)
        patienter.append(total_patienter)
        behandlede_patienter.append(årlige_patienter_us + årlige_patienter_eu)
    
    return omsætning, omkostninger, patienter, behandlede_patienter

def beregn_værdiansættelse(fase, omkostninger, forventede_fremtidige_pengestrømme, diskonteringsrente, risikofaktorer):
    """
    Beregner værdiansættelsen af IP'en på et specifikt stadie.

    Argumenter:
    fase (str): Udviklingsfasen der værdisættes.
    omkostninger (list): Liste over omkostninger.
    forventede_fremtidige_pengestrømme (list): Liste over forventede fremtidige pengestrømme.
    diskonteringsrente (float): Diskonteringsrente til NPV-beregning.
    risikofaktorer (list): Liste over risikofaktorer for hver periode.

    Returnerer:
    float: Risikojusteret nettonutidsværdi (rNPV) for fasen.
    """
    totale_omkostninger = sum(omkostninger)
    risikojusterede_pengestrømme = [cf * (1 - risikofaktorer[i]) for i, cf in enumerate(forventede_fremtidige_pengestrømme)]
    npv = npf.npv(diskonteringsrente, [-totale_omkostninger] + risikojusterede_pengestrømme)
    return npv

def beregn_aldersdistribution(lowe_syndrom_data, år):
    """
    Beregner aldersdistributionen for Lowe Syndrom patienter i et givet år.

    Argumenter:
    lowe_syndrom_data (dict): Fremskrevne Lowe Syndrom-populationsdata.
    år (int): Året for hvilket aldersdistributionen skal beregnes.

    Returnerer:
    list: Antal patienter i hver aldersgruppe.
    """
    aldersdistribution = [0] * 41  # 0 til 40 år
    for region, data in lowe_syndrom_data.items():
        for patient in data[år - 2023]:  # år - 2023 giver det korrekte indeks
            _, _, alder = patient
            if alder <= 40:
                aldersdistribution[alder] += 1
    return aldersdistribution

def beregn_risikojusteret_npv(pengestrømme, risikofaktorer, diskonteringsrente):
    """
    Beregner den risikojusterede NPV.
    
    Argumenter:
    pengestrømme (list): Liste over pengestrømme
    risikofaktorer (list): Liste over risikofaktorer for hver pengestrøm
    diskonteringsrente (float): Diskonteringsrente
    
    Returnerer:
    float: Risikojusteret NPV
    """
    risikojusterede_pengestrømme = [cf * (1 - rf) for cf, rf in zip(pengestrømme, risikofaktorer)]
    return npf.npv(diskonteringsrente, risikojusterede_pengestrømme)

def beregn_markedsstørrelse(prævalens, befolkning, pris, markedspenetration):
    """
    Beregner den potentielle markedsstørrelse.
    
    Argumenter:
    prævalens (float): Sygdommens prævalens
    befolkning (int): Samlet befolkning
    pris (float): Pris per behandling
    markedspenetration (float): Forventet markedspenetration
    
    Returnerer:
    float: Potentiel markedsstørrelse i kroner
    """
    antal_patienter = prævalens * befolkning
    return antal_patienter * pris * markedspenetration

def monte_carlo_simulation(antal_simuleringer, lowe_syndrom_data, simuleringsparametre):
    """
    Udfører en detaljeret Monte Carlo-simulation af lægemiddeludviklingen.
    
    Argumenter:
    antal_simuleringer (int): Antal simuleringer der skal udføres.
    lowe_syndrom_data (dict): Fremskrevne Lowe Syndrom-populationsdata.
    simuleringsparametre (dict): Ordbog med simuleringsparametre.
    
    Returnerer:
    list: Liste over resultater fra hver simulering.
    """
    resultater = []
    alle_patienter = []
    alle_behandlede_patienter = []
    for _ in range(antal_simuleringer):
        samlet_tid = 0
        samlede_omkostninger = 0
        fase_resultater = {}
        prv_værdi = 0 
        
        # Præklinisk fase
        præklinisk_succes, præklinisk_omkostninger, præklinisk_tid = simuler_fase(
            simuleringsparametre['præklinisk_succes_sandsynlighed'],
            simuleringsparametre['præklinisk_omkostningsinterval'],
            simuleringsparametre['præklinisk_tidsinterval']
        )
        samlet_tid += præklinisk_tid
        samlede_omkostninger += præklinisk_omkostninger

        præklinisk_omkostninger = np.random.uniform(*simuleringsparametre['præklinisk_omkostningsinterval'])
        fase1_omkostninger = np.random.uniform(*simuleringsparametre['fase1_omkostningsinterval'])
        fase2_omkostninger = np.random.uniform(*simuleringsparametre['fase2_omkostningsinterval'])
        fase3_omkostninger = np.random.uniform(*simuleringsparametre['fase3_omkostningsinterval'])
        godkendelse_omkostninger = np.random.uniform(*simuleringsparametre['godkendelse_omkostningsinterval'])

        odd_obtained = np.random.random() < simuleringsparametre['odd_probability']
        rpdd_obtained = np.random.random() < simuleringsparametre['rpdd_probability']
        
        if odd_obtained:
            cost_reduction = 1 - simuleringsparametre['odd_cost_reduction']
            præklinisk_omkostninger *= cost_reduction
            fase1_omkostninger *= cost_reduction
            fase2_omkostninger *= cost_reduction
            fase3_omkostninger *= cost_reduction
            godkendelse_omkostninger = min(godkendelse_omkostninger, 2e6)
            
        if præklinisk_succes:
            # Fase 1
            fase1_succes, fase1_omkostninger, fase1_tid = simuler_fase(
                simuleringsparametre['fase1_succes_sandsynlighed'],
                simuleringsparametre['fase1_omkostningsinterval'],
                simuleringsparametre['fase1_tidsinterval']
            )
            samlet_tid += fase1_tid
            samlede_omkostninger += fase1_omkostninger
            
            if fase1_succes:
                # Fase 2
                fase2_succes, fase2_omkostninger, fase2_tid = simuler_fase(
                    simuleringsparametre['fase2_succes_sandsynlighed'],
                    simuleringsparametre['fase2_omkostningsinterval'],
                    simuleringsparametre['fase2_tidsinterval']
                )
                samlet_tid += fase2_tid
                samlede_omkostninger += fase2_omkostninger
                
                if fase2_succes:
                    # Fase 3
                    fase3_succes, fase3_omkostninger, fase3_tid = simuler_fase(
                        simuleringsparametre['fase3_succes_sandsynlighed'],
                        simuleringsparametre['fase3_omkostningsinterval'],
                        simuleringsparametre['fase3_tidsinterval']
                    )
                    samlet_tid += fase3_tid
                    samlede_omkostninger += fase3_omkostninger
                    
                    if fase3_succes:
                        # Godkendelse
                        godkendelse_succes, godkendelse_omkostninger, godkendelse_tid = simuler_fase(
                            simuleringsparametre['godkendelse_succes_sandsynlighed'],
                            simuleringsparametre['godkendelse_omkostningsinterval'],
                            simuleringsparametre['godkendelse_tidsinterval']
                        )
                        samlet_tid += godkendelse_tid
                        samlede_omkostninger += godkendelse_omkostninger
                        
                        if godkendelse_succes:
                            # Beregn det år, hvor kommercialiseringen starter
                            kommercialiseringsår = 2023 + int(samlet_tid)
                            
                            # Beregn aldersdistribution for kommercialiseringsåret
                            aldersdistribution = beregn_aldersdistribution(lowe_syndrom_data, kommercialiseringsår)
                            
                            # Kommercialisering
                            markedsstørrelse_us = sum(aldersdistribution) * 0.5  # Assuming 50% of the market is in the US
                            markedsstørrelse_eu = sum(aldersdistribution) * 0.5  # Assuming 50% of the market is in the EU
                            
                            omsætning, omkostninger, patienter, behandlede_patienter = simuler_kommercialisering(
                                markedsstørrelse_us,
                                markedsstørrelse_eu,
                                simuleringsparametre['markedspenetration'],
                                simuleringsparametre['pris'],
                                simuleringsparametre['produktionsomkostning'],
                                simuleringsparametre['adoptionsparametre'],
                                simuleringsparametre['kommercialiseringsår'],
                                aldersdistribution
                            )
                            alle_patienter.append(patienter)
                            alle_behandlede_patienter.append(behandlede_patienter)

                            totale_omkostninger = samlede_omkostninger + sum(omkostninger)
                            total_omsætning = sum(omsætning)
                            
                            # Beregn burn rate
                            burn_rate = samlede_omkostninger / samlet_tid

                                                        # Adjust omsætning for RPDD voucher if obtained
                            if rpdd_obtained:
                                omsætning[0] += prv_værdi
                            
                            #Calculate cash flows
                            cash_flows = [-præklinisk_omkostninger, -fase1_omkostninger, -fase2_omkostninger, -fase3_omkostninger, -godkendelse_omkostninger] + omsætning
                            
                            # Prepare risk factors
                            risk_factors = [
                                1 - simuleringsparametre['præklinisk_succes_sandsynlighed'],
                                1 - simuleringsparametre['fase1_succes_sandsynlighed'],
                                1 - simuleringsparametre['fase2_succes_sandsynlighed'],
                                1 - simuleringsparametre['fase3_succes_sandsynlighed'],
                                1 - simuleringsparametre['godkendelse_succes_sandsynlighed'],
                                *simuleringsparametre['risikofaktorer']['godkendt']
                            ]
                            
                            # Calculate NPV for each phase
                            npvs = {}
                            for phase in ['præklinisk', 'fase1', 'fase2', 'fase3', 'godkendt']:
                                phase_index = ['præklinisk', 'fase1', 'fase2', 'fase3', 'godkendt'].index(phase)
                                phase_cash_flows = cash_flows[phase_index:]
                                phase_risk_factors = risk_factors[phase_index:]
                                
                                npvs[f'{phase}_npv'] = beregn_risikojusteret_npv(
                                    phase_cash_flows,
                                    phase_risk_factors,
                                    simuleringsparametre['diskonteringsrente']
                                )
                            
                            # Calculate ROI for each phase
                            rois = {}
                            cumulative_costs = np.cumsum([-cf for cf in cash_flows[:5] if cf < 0])  # Cumulative costs up to approval
                            for i, phase in enumerate(['præklinisk', 'fase1', 'fase2', 'fase3', 'godkendt']):
                                if cumulative_costs[i] > 0:
                                    rois[f'{phase}_roi'] = npvs[f'{phase}_npv'] / cumulative_costs[i] - 1
                                else:
                                    rois[f'{phase}_roi'] = float('inf')
                            
                            # Update the resultater dictionary
                            resultater.append({
                                **npvs,
                                **rois,
                                'præklinisk_omkostninger': præklinisk_omkostninger,
                                'fase1_omkostninger': fase1_omkostninger,
                                'fase2_omkostninger': fase2_omkostninger,
                                'fase3_omkostninger': fase3_omkostninger,
                                'godkendelse_omkostninger': godkendelse_omkostninger,            
                                'totale_omkostninger': totale_omkostninger,
                                'total_omsætning': total_omsætning,
                                'burn_rate': burn_rate,
                                'præklinisk_tid': præklinisk_tid,
                                'fase1_tid': fase1_tid,
                                'fase2_tid': fase2_tid,
                                'fase3_tid': fase3_tid,
                                'godkendelse_tid': godkendelse_tid,       
                                'samlet_tid': samlet_tid,
                                'odd_obtained': odd_obtained,
                                'rpdd_obtained': rpdd_obtained,
                                'prv_value': prv_værdi,
                            })
    return resultater,alle_patienter, alle_behandlede_patienter


def plot_patient_adoption(patienter, behandlede_patienter, adoptionsparametre, år):
    år_range = range(år)
    plt.figure(figsize=(12, 8))
    plt.plot(år_range, patienter, label='Total Lowe syndrom population', marker='o')
    plt.plot(år_range, behandlede_patienter, label='Behandlede patienter', marker='s')
    plt.title('Udvikling i Lowe syndrom population og behandlede patienter')
    plt.xlabel('År efter lancering')
    plt.ylabel('Antal patienter')
    plt.legend()
    plt.grid(True)
    #plt.fill_between(år_range, behandlede_patienter, patienter, alpha=0.3, label='Ubehandlede patienter')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Beregn og vis adoptionsrate
    actual_adoptionsrate = [treated / total if total > 0 else 0 for treated, total in zip(behandlede_patienter, patienter)]
    
    # Generate theoretical adoption curves
    us_adoption = generer_adoptionsrate(år, adoptionsparametre['us']['maks_adoption'], 
                                        adoptionsparametre['us']['forsinkelse'], 
                                        adoptionsparametre['us']['hastighed'])
    eu_adoption = generer_adoptionsrate(år, adoptionsparametre['eu']['maks_adoption'], 
                                        adoptionsparametre['eu']['forsinkelse'], 
                                        adoptionsparametre['eu']['hastighed'])
    
    plt.figure(figsize=(12, 8))
    plt.plot(år_range, actual_adoptionsrate, label='Actual Adoptionsrate', marker='o')
    plt.plot(år_range, us_adoption, label='Theoretical US Adoption', linestyle='--')
    plt.plot(år_range, eu_adoption, label='Theoretical EU Adoption', linestyle='--')
    plt.title('Adoptionsrate over tid')
    plt.xlabel('År efter lancering')
    plt.ylabel('Adoptionsrate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def run_simulation_with_varied_param(base_params, param_name, variation,lowe_syndrom_data):
    new_params = base_params.copy()
    
    def vary_param(param, variation):
        if isinstance(param, (int, float)):
            return param * (1 + variation)
        elif isinstance(param, dict):
            return {k: vary_param(v, variation) for k, v in param.items()}
        else:
            return param  # Return unchanged if it's neither numeric nor dict
    
    new_params[param_name] = vary_param(base_params[param_name], variation)
    
    # Run simulation with new params and return NPV
    results, _, _ = monte_carlo_simulation(1000, lowe_syndrom_data, new_params)
    return np.mean([r['godkendt_npv'] for r in results])

def calculate_parameter_impacts(resultater,base_params,lowe_syndrom_data, variation=0.1):
    base_npv = np.mean([r['godkendt_npv'] for r in resultater])
    impacts = {}
    
    for param in base_params:
        if param not in ['risikofaktorer', 'kommercialiseringsår']:  # Skip complex parameters
            new_npv = run_simulation_with_varied_param(base_params, param, variation,lowe_syndrom_data)
            impacts[param] = new_npv - base_npv
    
    return impacts

def plot_impact_chart(impacts):
    params = list(impacts.keys())
    values = list(impacts.values())
    
    # Sort by absolute impact
    sorted_indices = np.argsort(np.abs(values))
    params = [params[i] for i in sorted_indices]
    values = [values[i] for i in sorted_indices]
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create color map
    colors = ['red' if v < 0 else 'green' for v in values]
    
    # Plot horizontal bars
    y_pos = np.arange(len(params))
    ax.barh(y_pos, values, align='center', color=colors, alpha=0.8)
    
    # Customize the chart
    ax.set_xlabel('Change in NPV ($)')
    ax.set_title('Impact of 10% Increase in Parameters on NPV')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params)
    
    # Add value labels to the end of each bar
    for i, v in enumerate(values):
        ax.text(v, i, f'${v:,.0f}', va='center', fontweight='bold')
    
    # Add a vertical line for zero
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
    
    # Adjust layout and display
    plt.tight_layout()
    plt.show()