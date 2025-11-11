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
    
def calculate_survival_probability(age, median_survival=30, shape=2):
    """
    Calculate survival probability using Weibull distribution.
    Should be highest at age 0 and decrease with age.
    """
    if age >= 60:
        return 0
        
    # Use complementary Weibull CDF for survival probability
    # This gives probability of surviving TO this age
    return weibull_min.sf(age, shape, loc=0, 
                         scale=median_survival/(np.log(2)**(1/shape)))

def calculate_annual_mortality(age, median_survival=30, shape=2):
    """
    Calculate probability of dying during the next year at given age.
    Uses ratio of survival probabilities between current age and next age.
    """
    if age >= 60:
        return 1.0
        
    current_survival = calculate_survival_probability(age)
    next_survival = calculate_survival_probability(age + 1)
    
    # Probability of dying this year = 1 - P(survive this year)
    # P(survive this year) = P(survive to age+1) / P(survive to age)
    annual_mortality = 1 - (next_survival / current_survival) if current_survival > 0 else 1.0
    
    return max(0, min(1, annual_mortality))

def lowe_syndrom_fremskrivning(befolkningsdata, regioner, prævalens, maks_levetid, form, skala):
    """
    Fremskriver Lowe Syndrom-populationen over tid for flere regioner.
    
    Parametre:
    - befolkningsdata: DataFrame med befolkningstal per region/år/alder
    - regioner: Liste af regioner der skal inkluderes
    - prævalens: Sygdommens prævalens (fx 1/500000)
    - maks_levetid: Maksimal levealder for patienter
    - form: Weibull-fordelingens form-parameter for aldersfordeling
    - skala: Weibull-fordelingens skala-parameter for aldersfordeling
    """
    
    def get_diagnose_sandsynlighed(alder):
        """
        Returnerer andelen af udiagnosticerede cases der opdages ved hver alder.
        Sandsynlighederne er betingede - dvs. ud af de resterende udiagnosticerede cases.
        
        Fordeling:
        - 67% fanges ved fødslen (0 år)
        - 20% fanges som 1-årige
        - 8% fanges som 2-årige
        - 3% fanges som 3-årige
        - 1% fanges som 4-årige
        - 0.5% fanges som 5-årige
        - 0.5% fanges efter 5 år (meget sjældent)
        """
        if alder == 0:
            return 0.67    # 2/3 fanges ved fødslen
        elif alder == 1:
            return 0.20    # 20% af resterende fanges som 1-årige
        elif alder == 2:
            return 0.08    # 8% af resterende fanges som 2-årige
        elif alder == 3:
            return 0.03    # 3% af resterende fanges som 3-årige
        elif alder == 4:
            return 0.01    # 1% af resterende fanges som 4-årige
        elif alder == 5:
            return 0.005   # 0.5% af resterende fanges som 5-årige
        else:
            return 0.001   # Meget sjældent at fange cases efter 5 år

    # Initialiser datastruktur til at gemme patientdata
    lowe_syndrom_data = {}
    
    for region in regioner:
        print(f"\nBehandler region: {region}")
        lowe_syndrom_data[region] = []
        nuværende_id = 0
        udiagnosticerede_per_årgang = {}  # Dict til at holde styr på resterende cases per årgang
        
        # Filtrer befolkningsdata for denne region
        region_data = befolkningsdata[befolkningsdata['region'] == region]
        
        for år in range(2023, 2100):
            nuværende_års_data = []
            
            if år == 2023:
                # --- INITIAL POPULATION 2023 ---
                # Beregn total befolkning og forventet antal cases
                total_befolkning_2023 = region_data[region_data['Time'] == 2023]['Value'].sum()
                lowe_syndrom_2023 = total_befolkning_2023 * prævalens
                
                # Opret aldersfordeling baseret på Weibull
                aldersinterval = np.arange(0, maks_levetid + 1)
                aldersfordeling = weibull_min.pdf(aldersinterval, form, loc=0, scale=skala)
                aldersfordeling /= aldersfordeling.sum()
                
                # Fordel initial population efter Weibull-fordeling
                lowe_syndrom_aldersfordeling_2023 = np.round(lowe_syndrom_2023 * aldersfordeling)
                
                # Opret initial population
                for alder, antal in enumerate(lowe_syndrom_aldersfordeling_2023):
                    for _ in range(int(antal)):
                        nuværende_års_data.append((nuværende_id, år, alder, år - alder))
                        nuværende_id += 1
                
                print(f"Initial population oprettet: {len(nuværende_års_data)} patienter")
            
            else:
                # --- NYE FØDSLER ---
                fødsler = region_data.loc[
                    (region_data['Time'] == år) & (region_data["Age"] == "0"), 
                    'Value'
                ].sum()
                total_cases_årgang = fødsler * prævalens
                udiagnosticerede_per_årgang[år] = total_cases_årgang
                
                # --- DIAGNOSTICERING AF CASES ---
                # Gå igennem alle årgange der stadig kan have udiagnosticerede cases
                for fødselsår in list(udiagnosticerede_per_årgang.keys()):
                    alder = år - fødselsår
                    if alder <= 10:  # Vi diagnosticerer kun op til 10 års alderen
                        resterende_cases = udiagnosticerede_per_årgang[fødselsår]
                        if resterende_cases > 0:
                            diagnose_sandsynlighed = get_diagnose_sandsynlighed(alder)
                            antal_diagnosticeret = resterende_cases * diagnose_sandsynlighed
                            
                            # Tilføj de diagnosticerede cases
                            for _ in range(int(round(antal_diagnosticeret))):
                                nuværende_års_data.append((nuværende_id, år, alder, fødselsår))
                                nuværende_id += 1
                            
                            # Opdater resterende cases for årgangen
                            udiagnosticerede_per_årgang[fødselsår] -= antal_diagnosticeret
                    
                    # Fjern årgange der er færdigdiagnosticerede eller over 10 år
                    if alder > 10 or udiagnosticerede_per_årgang[fødselsår] <= 0:
                        del udiagnosticerede_per_årgang[fødselsår]

            # --- ÆLDNING OG MORTALITET ---
            if år > 2023:
                overlevende = 0
                total_evalueret = 0
                
                for id, prev_år, alder, diagnose_år in lowe_syndrom_data[region][-1]:
                    if alder < maks_levetid:
                        total_evalueret += 1
                        dødelighed = calculate_annual_mortality(alder)
                        
                        # Overlever hvis random tal er større end dødelighed
                        if np.random.random() > dødelighed:
                            nuværende_års_data.append((id, år, alder + 1, diagnose_år))
                            overlevende += 1
                
                if total_evalueret > 0:
                    overlevelsesrate = (overlevende / total_evalueret) * 100
                    print(f"Overlevelsesrate: {overlevelsesrate:.1f}%")

            # Gem årets data
            lowe_syndrom_data[region].append(nuværende_års_data)
            print(f"Total population ved udgangen af {år}: {len(nuværende_års_data)}")

    return pd.DataFrame([
        {
            'patient_id': id,
            'year': år,
            'age': alder,
            'diagnosis_year': diagnose_år,
            'region': region
        }
        for region, region_data in lowe_syndrom_data.items()
        for year_data in region_data
        for id, år, alder, diagnose_år in year_data
    ])

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
        fase12_omkostninger = np.random.uniform(*simuleringsparametre['fase12_omkostningsinterval'])
        fase3_omkostninger = np.random.uniform(*simuleringsparametre['fase3_omkostningsinterval'])
        godkendelse_omkostninger = np.random.uniform(*simuleringsparametre['godkendelse_omkostningsinterval'])

        odd_obtained = np.random.random() < simuleringsparametre['odd_fordele']['sandsynlighed']
        odd_benefits = {
                    'fee_savings': 0,
                    'tax_credits': 0,
                    'grant_amount': 0}
        
        rpdd_obtained = np.random.random() < simuleringsparametre['rpdd_probability']
        
        if odd_obtained:
            # 1. Gebyrfritagelser (påvirker godkendelsesomkostninger direkte)
            odd_benefits['fee_savings'] = simuleringsparametre['odd_fordele']['gebyr_fritagelser']
            godkendelse_omkostninger -= odd_benefits['fee_savings']
            
            # 2. Skattefradrag på kliniske omkostninger
            clinical_costs = fase12_omkostninger + fase3_omkostninger
            odd_benefits['tax_credits'] = clinical_costs * simuleringsparametre['odd_fordele']['skattefradrag']
            
            # 3. Forskningstilskud (hvis vi er heldige at få det)
            if np.random.random() < simuleringsparametre['odd_fordele']['forskningstilskud']['sandsynlighed']:
                odd_benefits['grant_amount'] = simuleringsparametre['odd_fordele']['forskningstilskud']['beløb']
                
        if præklinisk_succes:
            # Fase 1/2
            fase12_succes, fase12_omkostninger, fase12_tid = simuler_fase(
                simuleringsparametre['fase12_succes_sandsynlighed'],
                simuleringsparametre['fase12_omkostningsinterval'],
                simuleringsparametre['fase12_tidsinterval']
            )
            samlet_tid += fase12_tid
            samlede_omkostninger += fase12_omkostninger
            
            if fase12_succes:
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
                        
                        # --- PATIENT-LEVEL TREATMENT LOGIC ---
                        # 1. Build a DataFrame of all patients alive at commercialization year
                        patient_rows = []
                        for region, data in lowe_syndrom_data.items():
                            for patient in data[kommercialiseringsår - 2023]:
                                id, year, age, birth_year = patient
                                patient_rows.append({'patient_id': id, 'region': region, 'year': year, 'age': age, 'birth_year': birth_year, 'treated': False})
                        patients_df = pd.DataFrame(patient_rows)
                        
                        # 2. Simulate each year of commercialization
                        years_of_commercialization = simuleringsparametre['kommercialiseringsår']
                        adoptionsparametre = simuleringsparametre['adoptionsparametre']
                        pris = simuleringsparametre['pris']
                        produktionsomkostning = simuleringsparametre['produktionsomkostning']
                        markedspenetration = simuleringsparametre['markedspenetration']
                        
                        omsætning = []
                        omkostninger = []
                        patienter = []
                        behandlede_patienter = []
                        
                        omsætning_us = generer_adoptionsrate(years_of_commercialization, 
                            adoptionsparametre['us']['maks_adoption'], 
                            adoptionsparametre['us']['forsinkelse'], 
                            adoptionsparametre['us']['hastighed'])
                        omsætning_eu = generer_adoptionsrate(years_of_commercialization, 
                            adoptionsparametre['eu']['maks_adoption'], 
                            adoptionsparametre['eu']['forsinkelse'], 
                            adoptionsparametre['eu']['hastighed'])
                        
                        for år_index in range(years_of_commercialization):
                            # Only consider patients who are alive, untreated, and eligible (e.g., by age)
                            eligible_patients = patients_df[(patients_df['treated'] == False) & (patients_df['age'] < 21)]
                            total_patienter = len(eligible_patients)
                            patienter.append(total_patienter)
                            
                            # Calculate number to treat this year (US/EU split)
                            årlige_patienter_us = total_patienter * markedspenetration * omsætning_us[år_index] * 0.5
                            årlige_patienter_eu = total_patienter * markedspenetration * omsætning_eu[år_index] * 0.5

                            n_to_treat = int(round(årlige_patienter_us + årlige_patienter_eu))
                            # If more to treat than eligible, cap at eligible
                            n_to_treat = min(n_to_treat, total_patienter)
                            
                            # Randomly select patients to treat
                            if n_to_treat > 0 and total_patienter > 0:
                                treated_indices = eligible_patients.sample(n=n_to_treat, replace=False).index
                                patients_df.loc[treated_indices, 'treated'] = True
                            
                            behandlede_patienter.append(n_to_treat)
                            omsætning.append(n_to_treat * pris)
                            omkostninger.append(n_to_treat * produktionsomkostning)
                            
                            # Age all patients by 1 year for next cycle
                            patients_df['age'] += 1
                        
                        alle_patienter.append(patienter)
                        alle_behandlede_patienter.append(behandlede_patienter)

                        totale_omkostninger = samlede_omkostninger + sum(omkostninger)
                        total_omsætning = sum(omsætning)
                        
                        # Beregn burn rate
                        burn_rate = samlede_omkostninger / samlet_tid

                        # Adjust omsætning for RPDD voucher if obtained
                        if rpdd_obtained:
                            omsætning[0] += prv_værdi
                        
                        # Beregn cash flows med ODD fordele
                        cash_flows = [
                            -præklinisk_omkostninger,  # År 0
                            -fase12_omkostninger,      # År 1
                            -fase3_omkostninger,       # År 2
                            -godkendelse_omkostninger  # År 3
                        ]
                        for year_revenue in omsætning:
                            cash_flows.append(year_revenue)  # Add annual revenues

                        # If ODD benefits exist, add them
                        if odd_obtained:
                            # Add immediate fee savings to approval year
                            cash_flows[3] += odd_benefits['fee_savings']
                            
                            # Add tax credits in the appropriate years
                            tax_credit_fase12 = odd_benefits['tax_credits'] / 2
                            tax_credit_fase3 = odd_benefits['tax_credits'] / 2
                            
                            fase12_tax_year = 1 + simuleringsparametre['odd_fordele']['timing']['fase12']
                            fase3_tax_year = 2 + simuleringsparametre['odd_fordele']['timing']['fase3']
                            
                            # Extend cash_flows if needed
                            while len(cash_flows) <= max(fase12_tax_year, fase3_tax_year):
                                cash_flows.append(0)
                            
                            cash_flows[fase12_tax_year] += tax_credit_fase12
                            cash_flows[fase3_tax_year] += tax_credit_fase3
                            
                            # Add grant money if received
                            if odd_benefits['grant_amount'] > 0:
                                grant_per_year = odd_benefits['grant_amount'] / simuleringsparametre['odd_fordele']['forskningstilskud']['varighed']
                                for i in range(4):
                                    if i >= len(cash_flows):
                                        cash_flows.append(grant_per_year)
                                    else:
                                        cash_flows[i] += grant_per_year

                        # Prepare risk factors
                        risk_factors = [
                            1 - simuleringsparametre['præklinisk_succes_sandsynlighed'],
                            1 - simuleringsparametre['fase12_succes_sandsynlighed'],
                            1 - simuleringsparametre['fase3_succes_sandsynlighed'],
                            1 - simuleringsparametre['godkendelse_succes_sandsynlighed'],
                            *simuleringsparametre['risikofaktorer']['godkendt']
                        ]

                        # Calculate NPV for each phase
                        npvs = {}
                        for phase in ['præklinisk', 'fase12', 'fase3', 'godkendt']:
                            phase_index = ['præklinisk', 'fase12', 'fase3', 'godkendt'].index(phase)
                            phase_cash_flows = cash_flows[phase_index:]  # Include all future cash flows
                            phase_risk_factors = risk_factors[phase_index:]
                            
                            # Calculate NPV with all future cash flows
                            npvs[f'{phase}_npv'] = beregn_risikojusteret_npv(
                                phase_cash_flows,
                                phase_risk_factors + [risk_factors[-1]] * (len(phase_cash_flows) - len(phase_risk_factors)),  # Extend risk factors if needed
                                simuleringsparametre['diskonteringsrente']
                            )
                        # Calculate ROI for each phase
                        rois = {}
                        # Get all costs up to approval (first 4 elements, make them negative if they aren't already)
                        phase_costs = [-cf if cf > 0 else cf for cf in cash_flows[:4]]
                        cumulative_costs = np.cumsum([-c for c in phase_costs])  # Make all positive for ROI calc

                        for i, phase in enumerate(['præklinisk', 'fase12', 'fase3', 'godkendt']):
                            if i < len(cumulative_costs) and cumulative_costs[i] > 0:
                                rois[f'{phase}_roi'] = npvs[f'{phase}_npv'] / cumulative_costs[i] - 1
                            else:
                                rois[f'{phase}_roi'] = float('inf')  # or 0, depending on your preference
                        # Update the resultater dictionary
                        resultater.append({
                            **npvs,
                            **rois,
                            'præklinisk_omkostninger': præklinisk_omkostninger,
                            'fase12_omkostninger': fase12_omkostninger,
                            'fase3_omkostninger': fase3_omkostninger,
                            'godkendelse_omkostninger': godkendelse_omkostninger,            
                            'totale_omkostninger': totale_omkostninger,
                            'total_omsætning': total_omsætning,
                            'burn_rate': burn_rate,
                            'præklinisk_tid': præklinisk_tid,
                            'fase12_tid': fase12_tid,
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