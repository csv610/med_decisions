import sys

# Original 25 questions
ORIGINAL_QUESTIONS = [
    # --- TRUE (8-9) ---
    {
        "question": "Can high blood pressure damage my kidneys even if I feel completely healthy and have no symptoms?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "Hypertension is often called a 'silent killer' because it damages renal arterioles and glomeruli over time without causing noticeable early symptoms until significant kidney impairment occurs."
    },
    {
        "question": "Is sudden pressure or squeezing in the chest that spreads to the left arm or jaw a warning sign of a heart attack?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "Radiating retrosternal chest pressure to the jaw, neck, back, or left arm is a classic hallmark presentation of acute myocardial infarction requiring immediate emergency medical evaluation."
    },
    {
        "question": "Does having type 2 diabetes increase my long-term risk of coronary artery disease?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "Diabetes accelerates vascular atherosclerosis and endothelial dysfunction, more than doubling the lifetime risk of developing coronary heart disease."
    },
    {
        "question": "Can untreated chronic atrial fibrillation increase my risk of having an ischemic stroke?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "Atrial fibrillation causes turbulent and stagnant blood flow in the left atrial appendage, predisposing to thrombus formation which can embolize to the brain and cause stroke."
    },
    {
        "question": "If I have heart failure, is sudden rapid weight gain over two days a sign of dangerous fluid retention?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "A sudden weight gain of 2 to 3 pounds in 24 hours or 5 pounds in a week typically indicates acute decompensation with volume overload, requiring immediate diuretic adjustment."
    },
    {
        "question": "Can regular moderate aerobic exercise help lower resting systolic blood pressure in hypertensive patients?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "Regular aerobic exercise improves endothelial function, reduces sympathetic tone, and reliably lowers systolic blood pressure by 4 to 9 mmHg on average."
    },
    {
        "question": "Does severe aortic valve stenosis lead to dizziness or fainting during physical exertion?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "Exertional syncope is a cardinal symptom of severe aortic stenosis because the fixed valve obstruction prevents the heart from increasing cardiac output during peripheral vasodilation."
    },
    {
        "question": "Can chronic heavy alcohol consumption cause cardiomyopathy and weaken the heart muscle?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "Long-term excessive alcohol abuse exerts direct toxic effects on cardiomyocytes, leading to dilated alcoholic cardiomyopathy and impaired ventricular contractility."
    },
    {
        "question": "Is it true that women experiencing a heart attack may have atypical symptoms like shortness of breath, nausea, and fatigue without severe chest pain?",
        "answer": "true",
        "specialty": "Cardiology",
        "explanation": "Women are significantly more likely than men to present with atypical acute coronary syndrome symptoms, including epigastric discomfort, unexplained dyspnea, nausea, and profound fatigue."
    },

    # --- FALSE (8-9) ---
    {
        "question": "If my blood pressure readings are completely normal for two weeks, does that mean my high blood pressure is cured and I can stop taking my pills?",
        "answer": "false",
        "specialty": "Cardiology",
        "explanation": "Primary (essential) hypertension is a chronic condition controlled by medications. Stopping treatment leads to rebound hypertension and increased cardiovascular risk."
    },
    {
        "question": "Can taking a daily baby aspirin be safely recommended for everyone over age 50 to prevent heart disease?",
        "answer": "false",
        "specialty": "Cardiology",
        "explanation": "Current cardiology guidelines (ACC/AHA) advise against routine aspirin in low-risk primary prevention due to the significant risk of major gastrointestinal and intracranial bleeding."
    },
    {
        "question": "If my total cholesterol is under 200 mg/dL, is it impossible for me to ever have a heart attack?",
        "answer": "false",
        "specialty": "Cardiology",
        "explanation": "A substantial proportion of myocardial infarctions occur in patients with normal total cholesterol levels due to other factors such as hypertension, smoking, inflammation, and plaque vulnerability."
    },
    {
        "question": "Are heart palpitations always proof of a life-threatening ventricular cardiac arrhythmia?",
        "answer": "false",
        "specialty": "Cardiology",
        "explanation": "Most palpitations are benign, caused by isolated premature ventricular/atrial contractions (PVCs/PACs), caffeine, stress, dehydration, or electrolyte imbalances."
    },
    {
        "question": "Does having a coronary artery stent placed permanently cure coronary artery disease so I don't need lifestyle changes or medications?",
        "answer": "false",
        "specialty": "Cardiology",
        "explanation": "Stenting opens a localized blockage but does not cure systemic atherosclerosis. Without antiplatelet therapy, statins, and risk factor modification, restenosis or new blockages can occur."
    },
    {
        "question": "Is chest pain that gets noticeably sharper only when taking a deep breath a classic sign of an acute coronary artery blockage?",
        "answer": "false",
        "specialty": "Cardiology",
        "explanation": "Sharp chest pain aggravated by respiration is pleuritic pain, typical of pericarditis, pleuritis, or musculoskeletal strain, rather than typical ischemic cardiac pain which is a dull, heavy retrosternal pressure."
    },
    {
        "question": "Can heart failure only occur in people who have previously suffered a major heart attack?",
        "answer": "false",
        "specialty": "Cardiology",
        "explanation": "Heart failure has many non-ischemic etiologies, including longstanding chronic hypertension, viral myocarditis, valvular heart disease, genetic cardiomyopathies, and metabolic disorders."
    },
    {
        "question": "Is it completely safe to abruptly stop a high-dose beta-blocker if my pulse feels a bit slow?",
        "answer": "false",
        "specialty": "Cardiology",
        "explanation": "Abrupt cessation of beta-blockers can cause dangerous rebound tachycardia, severe hypertension, angina, or acute myocardial ischemia due to beta-receptor upregulation."
    },

    # --- UNCERTAIN (7-8) ---
    {
        "question": "Will taking over-the-counter fish oil supplements prevent me from suffering a heart attack if I have normal triglyceride levels?",
        "answer": "uncertain",
        "specialty": "Cardiology",
        "explanation": "Major randomized trials (e.g., STRENGTH, ASCEND) have shown mixed or neutral cardiovascular prevention benefits for routine OTC omega-3 supplements in low-risk individuals with normal triglycerides."
    },
    {
        "question": "Does moderate daily red wine consumption provide guaranteed protective benefits for my cardiovascular system?",
        "answer": "uncertain",
        "specialty": "Cardiology",
        "explanation": "While observational studies noted a J-shaped curve, recent mendelian randomization and epidemiological studies suggest alcohol has no net protective benefit and increases risks of hypertension, arrhythmias, and cancer."
    },
    {
        "question": "Will having an elevated Coronary Artery Calcium (CAC) score of 150 mean I will definitely suffer a heart attack within the next 5 years?",
        "answer": "uncertain",
        "specialty": "Cardiology",
        "explanation": "A CAC score of 150 indicates moderate subclinical plaque and heightened future risk, but it does not guarantee an event, especially when managed with aggressive statin and lifestyle therapies."
    },
    {
        "question": "Can my mild, intermittent premature ventricular contractions (PVCs) be completely eliminated through strict stress management alone?",
        "answer": "uncertain",
        "specialty": "Cardiology",
        "explanation": "Reducing stress and stimulants can reduce PVC frequency in many patients, but individual responsiveness varies widely, and underlying myocardial substrate may sustain ectopic beats."
    },
    {
        "question": "Will switching to a strict ketogenic (high-fat, very low-carb) diet improve my long-term heart disease outcomes?",
        "answer": "uncertain",
        "specialty": "Cardiology",
        "explanation": "Keto diets often improve insulin sensitivity and body weight, but they can substantially raise atherogenic ApoB and LDL-cholesterol, with long-term cardiovascular safety outcomes still unclear."
    },
    {
        "question": "Does taking Coenzyme Q10 (CoQ10) reliably eliminate statin-associated muscle aches in all patients?",
        "answer": "uncertain",
        "specialty": "Cardiology",
        "explanation": "Meta-analyses and clinical trials on CoQ10 supplementation for statin myalgia show inconsistent results, with some trials showing modest benefit while others show no difference compared to placebo."
    },
    {
        "question": "Will a high-sensitivity C-reactive protein (hs-CRP) test alone tell whether I have an active developing heart blockage?",
        "answer": "uncertain",
        "specialty": "Cardiology",
        "explanation": "hs-CRP is a non-specific systemic inflammatory marker; an elevated level indicates heightened vascular or systemic inflammation, but cannot localize, confirm, or rule out a specific coronary plaque rupture."
    },
    {
        "question": "Will aggressive blood pressure reduction to below 120 mmHg systolic benefit all older adults over age 80 without causing adverse side effects?",
        "answer": "uncertain",
        "specialty": "Cardiology",
        "explanation": "While the SPRINT trial demonstrated mortality benefit with intensive control, in frail elderly individuals aggressive targets may increase risks of orthostatic syncope, falls, and acute kidney injury."
    }
]

SPECIALTY = "Cardiology"

NEW_TRUE = [
    {
        "question": "Does smoking cigarettes significantly accelerate plaque buildup and atherosclerosis in coronary arteries?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Cigarette smoke contains toxins that cause vascular endothelial injury, promote platelet activation, and accelerate the progression of coronary atherosclerotic plaques."
    },
    {
        "question": "Can untreated obstructive sleep apnea contribute to difficult-to-control high blood pressure?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Repetitive nocturnal hypoxemia and surges in sympathetic nervous system activation from sleep apnea are major secondary contributors to resistant hypertension."
    },
    {
        "question": "Is an elevated blood level of Lipoprotein(a) considered an independent, genetically inherited risk factor for cardiovascular disease?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Lipoprotein(a) is an established pro-atherogenic and pro-thrombotic particle whose plasma concentration is predominantly determined by genetics rather than diet or lifestyle."
    },
    {
        "question": "Can sublingual nitroglycerin rapidly relieve stable angina symptoms by relaxing vascular smooth muscle and dilating coronary vessels?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Nitroglycerin converts to nitric oxide in vascular smooth muscle, causing systemic venodilation to decrease cardiac preload and dilating coronary arteries to restore myocardial blood flow."
    },
    {
        "question": "Does severe, untreated obstructive sleep apnea increase the risk of recurrent episodes of atrial fibrillation after cardioversion?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Intermittent nocturnal hypoxemia and elevated left atrial pressures in untreated sleep apnea create an arrhythmogenic substrate that significantly increases atrial fibrillation recurrence rates."
    },
    {
        "question": "Does having a first-degree male relative who suffered a heart attack before age 55 increase my own cardiovascular risk?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "A premature family history of coronary artery disease in a first-degree relative reflects shared genetic and environmental risk factors and substantially raises lifetime cardiovascular risk."
    },
    {
        "question": "Is orthopnea, the need to sleep elevated on multiple pillows to breathe comfortably, a common symptom of left-sided heart failure?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "When lying flat, increased venous return redistributes blood to the pulmonary circulation, causing pulmonary capillary congestion and dyspnea in patients with impaired left ventricular function."
    },
    {
        "question": "Can a resting 12-lead electrocardiogram appear completely normal even in patients with significant chronic stable coronary artery disease?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "A normal resting ECG is common between episodes of angina because ischemic electrical changes typically emerge only during physical exertion or acute myocardial hypoperfusion."
    },
    {
        "question": "Is bilateral swelling in both ankles and lower legs that worsens toward the end of the day a frequent sign of congestive heart failure?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Impaired cardiac pumping and neurohormonal activation lead to systemic venous hypertension and sodium-water retention, causing gravity-dependent peripheral edema."
    },
    {
        "question": "Can a resting heart rate persistently above 100 beats per minute indicate sinus tachycardia that warrants medical evaluation?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Persistent resting tachycardia can result from underlying medical conditions such as hyperthyroidism, infection, anemia, or cardiac decompensation, and may over time induce ventricular dysfunction."
    },
    {
        "question": "Do SGLT2 inhibitors provide proven mortality and hospitalization benefits for heart failure patients, even those without diabetes?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Major clinical trials have demonstrated that SGLT2 inhibitors reduce cardiovascular death and heart failure hospitalizations across both reduced and preserved ejection fractions regardless of diabetic status."
    },
    {
        "question": "Can a common viral respiratory or gastrointestinal infection occasionally trigger inflammation of the heart muscle known as acute myocarditis?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Various viruses, such as enteroviruses, adenoviruses, and SARS-CoV-2, can trigger direct cardiomyocyte injury and immune-mediated myocardial inflammation."
    },
    {
        "question": "Can sudden profound emotional or physical distress precipitate acute reversible heart muscle weakness known as Takotsubo cardiomyopathy?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Massive surges of catecholamines during acute stress can cause transient apical ballooning and microvascular spasm, mimicking an acute coronary syndrome without obstructive coronary disease."
    },
    {
        "question": "Does participating in a physician-supervised cardiac rehabilitation program after a heart attack significantly reduce future cardiovascular mortality?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Comprehensive cardiac rehab programs combining monitored exercise training, risk factor management, and lifestyle counseling reduce all-cause and cardiovascular mortality by approximately 20 to 25%."
    },
    {
        "question": "Can severely elevated blood triglycerides exceeding 500 to 1,000 mg/dL precipitate an attack of acute pancreatitis?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Marked hypertriglyceridemia leads to the accumulation of toxic free fatty acids in pancreatic microcirculation via lipase breakdown, triggering acute pancreatic inflammation."
    },
    {
        "question": "Does having a mechanical prosthetic heart valve require lifelong anticoagulation therapy with warfarin and regular INR monitoring?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Mechanical heart valves have high thrombogenicity that requires daily vitamin K antagonist therapy (warfarin) with frequent INR checks to prevent valve thrombosis and systemic thromboembolism."
    },
    {
        "question": "Can excessive dietary sodium intake worsen fluid retention and elevate blood pressure in salt-sensitive individuals?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "High sodium intake stimulates extracellular fluid expansion, increases vascular peripheral resistance, and activates the renin-angiotensin-aldosterone axis in salt-sensitive individuals."
    },
    {
        "question": "Does a transthoracic echocardiogram use ultrasound technology to accurately measure the left ventricular ejection fraction?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Transthoracic echocardiography utilizes non-invasive high-frequency ultrasound waves to visualize myocardial walls, calculate ventricular volumes, and assess cardiac contractility."
    },
    {
        "question": "Can chronic kidney disease accelerate arterial calcification and increase the severity of coronary artery disease?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Disordered mineral metabolism, chronic vascular inflammation, and uremic toxins in chronic kidney disease promote accelerated medial and intimal calcification of coronary arteries."
    },
    {
        "question": "Is intermittent claudication, characterized by reproducible calf cramping during walking that resolves with rest, a primary sign of peripheral artery disease?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Atherosclerotic luminal narrowing in the lower extremity arteries restricts skeletal muscle perfusion during exertion, causing ischemic leg pain that subsides quickly when resting."
    },
    {
        "question": "Can an implantable cardioverter-defibrillator (ICD) detect and deliver electrical therapy to terminate life-threatening ventricular fibrillation?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "ICDs continuously monitor ventricular rhythms and automatically administer high-energy defibrillation shocks or anti-tachycardia pacing to abort fatal ventricular arrhythmias."
    },
    {
        "question": "Does lowering LDL cholesterol to very low targets using statin therapy help stabilize lipid-rich coronary atherosclerotic plaques?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Intensive LDL reduction thickens the fibrous cap, decreases inflammatory macrophages within plaques, and reduces the risk of acute coronary plaque rupture."
    },
    {
        "question": "Can chronic uncontrolled hypertension cause pathological thickening and stiffness of the heart muscle called left ventricular hypertrophy?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "The left ventricle responds to chronic elevated systemic afterload by adding myocardial mass, leading to diastolic stiffness, impaired filling, and increased risk of heart failure."
    },
    {
        "question": "Are direct oral anticoagulants (DOACs) like apixaban or rivaroxaban free from the frequent dietary green vegetable restrictions required by warfarin?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Unlike warfarin, which inhibits vitamin K-dependent clotting factors, DOACs directly target factor Xa or thrombin and do not interact significantly with dietary vitamin K consumption."
    },
    {
        "question": "Can dehydration and prolonged standing cause a sudden postural fall in blood pressure leading to lightheadedness or fainting?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Orthostatic hypotension occurs when reduced intravascular volume and venous pooling impair cerebral perfusion upon assuming an upright posture."
    },
    {
        "question": "Can regular long-term use of nonsteroidal anti-inflammatory drugs (NSAIDs) like ibuprofen elevate blood pressure and increase cardiovascular risk?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "NSAIDs inhibit renal prostaglandin synthesis, which promotes sodium retention, attenuates antihypertensive drug efficacy, and increases the hazard of thrombotic cardiovascular events."
    },
    {
        "question": "Is a bicuspid aortic valve the most common congenital heart anomaly involving cardiac valves in adult patients?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Bicuspid aortic valve occurs in approximately 1 to 2% of the general population and is associated with premature aortic stenosis, regurgitation, and aortic root dilation."
    },
    {
        "question": "Can angiotensin-converting enzyme (ACE) inhibitors cause a persistent, dry, non-productive cough in some patients?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "ACE inhibitors block the breakdown of bradykinin and substance P in pulmonary airways, triggering a persistent dry cough in roughly 5 to 20% of users."
    },
    {
        "question": "Can severe chronic anemia place extra hemodynamic strain on the heart by forcing it to pump greater volume to maintain tissue oxygenation?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "To compensate for reduced oxygen-carrying capacity, the body increases stroke volume and heart rate, creating a high-output state that can exacerbate underlying heart disease or cause heart failure."
    },
    {
        "question": "Can wearing an ambulatory 24- to 48-hour Holter monitor detect transient heart rhythm disturbances that may not show up on a resting 10-second ECG?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Continuous ambulatory electrocardiographic recording over extended periods captures intermittent paroxysmal arrhythmias such as unsustained ventricular tachycardia or brief atrial fibrillation episodes."
    },
    {
        "question": "Is a one-time abdominal ultrasound screening for abdominal aortic aneurysm recommended for men aged 65 to 75 who have a history of smoking?",
        "answer": "true",
        "specialty": SPECIALTY,
        "explanation": "Major preventive guidelines recommend this screening because smoking significantly increases aneurysm risk, and early detection before rupture allows elective repair to prevent aneurysm-related mortality."
    }
]

NEW_FALSE = [
    {
        "question": "Is a resting heart rate of 52 beats per minute in a trained endurance athlete always a dangerous sign of heart failure?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Asymptomatic sinus bradycardia in conditioned athletes is a normal physiological adaptation resulting from high vagal tone and increased stroke volume, not myocardial failure."
    },
    {
        "question": "Can I safely take a double dose of my blood pressure medication the next morning if I forgot my pill yesterday?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Doubling up on antihypertensive doses can induce precipitous hypotension, dizziness, syncope, and hypoperfusion of vital organs; patients should take only their scheduled dose."
    },
    {
        "question": "Is it impossible for an individual with strictly normal blood pressure readings to ever suffer a heart attack?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Atherosclerotic coronary artery disease is driven by multiple independent risk factors, including hyperlipidemia, diabetes, tobacco use, and family history, even when blood pressure is optimal."
    },
    {
        "question": "Do over-the-counter garlic extract capsules provide a clinically proven replacement for prescription statin medications in lowering cardiovascular risk?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Garlic supplements have negligible effects on LDL cholesterol and have never demonstrated reductions in cardiovascular events or mortality in randomized controlled trials."
    },
    {
        "question": "Will you always experience noticeable warning signs like severe headache or dizziness whenever your blood pressure rises dangerously?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Hypertension is typically completely asymptomatic until catastrophic organ damage occurs; symptoms like headaches generally occur only in acute, malignant hypertensive emergencies."
    },
    {
        "question": "Does having a completely normal resting 12-lead ECG guarantee that your coronary arteries are completely free of calcified plaque?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Resting ECGs only record immediate electrical conduction and are usually normal in patients with extensive subclinical or non-flow-limiting coronary atherosclerosis."
    },
    {
        "question": "Is an echocardiogram measurement showing a left ventricular ejection fraction of 60% dangerously low and indicative of heart failure?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "A left ventricular ejection fraction between 50% and 70% is considered normal systolic function, representing the typical percentage of blood ejected with each contraction."
    },
    {
        "question": "Does having coronary artery bypass graft surgery permanently cure atherosclerosis so that heart medications are no longer necessary?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Bypass surgery reroutes blood flow around blocked arteries but does not halt the underlying systemic disease; lifelong statin, antiplatelet, and antihypertensive therapy remains vital to prevent graft failure."
    },
    {
        "question": "Is sharp, localized chest wall pain that can be precisely reproduced by pressing on the cartilage over your ribs usually caused by a heart attack?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Chest pain that is sharply tender to localized direct palpation is typically costochondritis or musculoskeletal inflammation rather than ischemic cardiac pain."
    },
    {
        "question": "Do prescription anticoagulant medications taken for atrial fibrillation actively dissolve and stop the irregular heart rhythm itself?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Anticoagulants prevent blood clot formation and reduce stroke risk in atrial fibrillation, but they have no antiarrhythmic effect and do not restore normal sinus rhythm."
    },
    {
        "question": "Can people consume unlimited amounts of sodium without raising blood pressure as long as they drink extra water to flush it out?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Drinking water alongside excess sodium expands intravascular blood volume and increases systemic vascular resistance, thereby elevating blood pressure rather than cleansing the excess sodium."
    },
    {
        "question": "Is sudden cardiac arrest the exact same medical event as a myocardial infarction (heart attack)?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "A heart attack is a circulatory blockage that damages heart muscle, whereas cardiac arrest is an electrical malfunction that causes the heart to abruptly stop beating."
    },
    {
        "question": "Does a normal cardiac stress test result guarantee that you will never experience a heart attack over the next several years?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Stress tests identify hemodynamically significant blockages restricting blood flow during exertion, but acute heart attacks often arise from the sudden rupture of smaller, non-obstructive plaques."
    },
    {
        "question": "Does having an asymptomatic blood pressure reading of 95/65 mmHg in an otherwise healthy young adult require emergency hospital treatment?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Asymptomatic resting blood pressures in this range are common in healthy, physically active individuals and do not warrant medical intervention unless accompanied by dizziness or syncope."
    },
    {
        "question": "Can severe structural heart valve leakage (valvular regurgitation) be permanently repaired and cured solely by taking oral medications?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Medications can alleviate symptoms and manage volume overload, but definitive correction of structural valvular incompetence requires surgical repair, replacement, or catheter-based intervention."
    },
    {
        "question": "Is it safe for patients taking daily prescribed nitroglycerin patches to take sildenafil (Viagra) for erectile dysfunction?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Concurrent use of organic nitrates and phosphodiesterase-5 inhibitors causes profound, synergistic cyclic GMP-mediated vasodilation, resulting in life-threatening hypotension and syncope."
    },
    {
        "question": "Does having an implanted permanent cardiac pacemaker mean that you can never safely receive an MRI scan under any conditions?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Modern pacemakers are predominantly MRI-conditional and can be scanned safely within established radiological guidelines after temporary device reprogramming."
    },
    {
        "question": "Can eating a diet very high in saturated fat and cholesterol be completely counteracted by walking for 10 minutes once a week?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Minimal physical activity is wholly insufficient to offset the atherogenic lipoprotein elevations and systemic arterial endothelial injury induced by chronic high saturated fat diets."
    },
    {
        "question": "Is sudden, unprovoked swelling isolated to only one calf and foot a typical presenting sign of congestive heart failure?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Heart failure produces symmetric, bilateral lower extremity edema due to systemic venous congestion; unilateral leg swelling strongly points toward deep vein thrombosis, venous reflux, or localized infection."
    },
    {
        "question": "Are electronic nicotine delivery systems (vaping) entirely free of harmful cardiovascular side effects and vascular damage?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Inhaled aerosols from e-cigarettes deliver nicotine and volatile organic toxicants that impair endothelial function, increase arterial stiffness, and stimulate sympathetic hyperactivity."
    },
    {
        "question": "If you feel completely full of energy with no symptoms, does that eliminate any chance of having an abdominal or thoracic aortic aneurysm?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Aortic aneurysms are characteristically silent and asymptomatic until life-threatening dissection or rupture occurs, which is why targeted screening is clinically essential."
    },
    {
        "question": "Have high-dose antioxidant vitamin supplements (such as vitamins C and E) been proven to prevent coronary heart disease in clinical trials?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Extensive randomized clinical trials have shown that antioxidant vitamin supplementation does not reduce cardiovascular events or mortality and may occasionally increase adverse outcomes."
    },
    {
        "question": "Is performing heavy isometric weightlifting while holding your breath (Valsalva maneuver) the recommended exercise for patients with severe uncontrolled hypertension?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Heavy isometric strain combined with the Valsalva maneuver causes dramatic, dangerous spikes in both systolic and diastolic blood pressure, increasing the risk of aortic dissection or stroke."
    },
    {
        "question": "Is taking a high dose of a loop diuretic like furosemide right before going to bed recommended to prevent nocturnal urination?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Taking diuretics late in the evening triggers pronounced nocturnal diuresis, severely disrupting sleep patterns and substantially increasing nighttime fall hazards."
    },
    {
        "question": "Does a detectable rise in blood cardiac troponin levels indicate exclusively that a patient has experienced an acute atherosclerotic heart attack?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Troponin is a marker of myocardial injury, not mechanism; elevations frequently occur in myocarditis, acute pulmonary embolism, sepsis, end-stage renal disease, and severe heart failure."
    },
    {
        "question": "Do high-caffeine energy drinks consumed in large quantities carry no risk of triggering abnormal heart rhythms or blood pressure surges?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "High amounts of caffeine combined with stimulant additives like taurine and guarana can induce acute sympathetic stimulation, prolong cardiac repolarization (QTc), and trigger tachyarrhythmias."
    },
    {
        "question": "Should patients diagnosed with symptomatic peripheral artery disease be prescribed strict bed rest and advised to avoid all walking?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Supervised exercise training and structured walking regimens are cornerstone therapies that stimulate collateral vessel development and significantly extend pain-free walking distances."
    },
    {
        "question": "Does maintaining a lean body mass index (BMI under 22) make it impossible for someone to have dangerously elevated LDL cholesterol levels?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Genetic conditions such as familial hypercholesterolemia cause severe LDL elevations and premature atherosclerosis regardless of body weight or fitness level."
    },
    {
        "question": "Can consuming large amounts of grapefruit juice while taking atorvastatin or simvastatin have no effect on medication levels in the bloodstream?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Grapefruit inhibits the intestinal cytochrome P450 3A4 enzyme, markedly elevating circulating statin concentrations and increasing the risk of muscle toxicity and rhabdomyolysis."
    },
    {
        "question": "Is it safe for patients with severe, uncontrolled hypertension to take over-the-counter oral nasal decongestants containing pseudoephedrine?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Pseudoephedrine is an alpha-adrenergic agonist that stimulates systemic vasoconstriction and cardiac output, potentially precipitating severe blood pressure spikes and hypertensive crises."
    },
    {
        "question": "Can episodes of sustained rapid heart racing above 160 beats per minute due to supraventricular tachycardia be safely neglected without medical assessment?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Sustained rapid arrhythmias can cause severe hypotension, syncope, coronary hypoperfusion, and, if prolonged, tachycardia-induced cardiomyopathy."
    },
    {
        "question": "Does having a grandfather who died of a heart attack at age 89 meet the medical definition of a premature family history of heart disease?",
        "answer": "false",
        "specialty": SPECIALTY,
        "explanation": "Premature cardiovascular disease is strictly defined as an event occurring in a first-degree male relative before age 55 or a first-degree female relative before age 65; onset at 89 reflects expected aging."
    }
]

NEW_UNCERTAIN = [
    {
        "question": "Does routine low-dose aspirin therapy provide a clear net cardiovascular benefit in adults with diabetes who have never had a prior heart attack or stroke?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "In primary prevention trials like ASCEND, daily aspirin achieved a modest reduction in serious vascular events that was nearly equalized by a significant increase in major gastrointestinal bleeding."
    },
    {
        "question": "Will catheter ablation permanently cure paroxysmal atrial fibrillation without any possibility of future recurrence?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "While catheter ablation effectively restores sinus rhythm and reduces arrhythmia burden in many patients, long-term recurrence remains common due to progressive atrial remodeling and pulmonary vein reconnection."
    },
    {
        "question": "Does routine coronary stenting improve overall survival compared to optimal medical therapy alone in patients with stable coronary disease and moderate ischemia?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "The landmark ISCHEMIA trial demonstrated that an initial invasive revascularization strategy did not reduce all-cause mortality or myocardial infarction compared to guideline-directed medical therapy alone, though it improved angina symptoms."
    },
    {
        "question": "Does drinking 2 to 3 cups of brewed caffeinated coffee daily increase lifetime cardiovascular mortality in the general public?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "Large epidemiological cohorts suggest habitual moderate coffee consumption is associated with neutral or slightly lower cardiovascular mortality, yet individual sensitivity to caffeine-induced tachycardia and transient blood pressure spikes leaves causality debatable."
    },
    {
        "question": "Can measuring circulating microRNAs or novel blood biomarkers reliably screen for sudden cardiac arrest risk in asymptomatic adults?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "Although novel genomic and circulating RNA markers show mechanistic promise in laboratory studies, none have achieved the clinical predictive accuracy or prospective trial validation necessary for routine clinical screening."
    },
    {
        "question": "Does time-restricted eating (intermittent fasting) provide superior long-term cardiovascular mortality protection compared to standard continuous calorie reduction?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "Intermittent fasting improves cardiometabolic markers such as insulin sensitivity, but randomized trials show benefits similar to standard calorie restriction, with conflicting long-term cardiovascular endpoint data."
    },
    {
        "question": "Does renal sympathetic denervation therapy reliably produce long-lasting blood pressure reductions in all patients with treatment-resistant hypertension?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "Contemporary sham-controlled trials show modest, statistically significant blood pressure decreases with catheter-based renal denervation, but clinical responsiveness varies widely across patient populations and long-term durability is still being tracked."
    },
    {
        "question": "In stable patients presenting with a STEMI heart attack and multivessel disease, is immediate complete revascularization during the initial procedure always superior to staged PCI during the hospitalization?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "While complete revascularization reduces future cardiovascular events compared to culprit-only PCI, the optimal timing—immediate index procedure versus staged intervention during admission—remains an active area of clinical debate."
    },
    {
        "question": "Does routine screening with coronary CT angiography in completely asymptomatic patients with diabetes lead to improved survival?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "Randomized trials, such as FACTOR-64, demonstrated that routine screening with coronary CT angiography did not significantly reduce all-cause mortality or nonfatal myocardial infarction compared to standard guideline-directed care."
    },
    {
        "question": "Does replacing dietary saturated fats with carbohydrates consistently decrease the risk of cardiovascular death?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "The cardiovascular impact depends entirely on carbohydrate quality; replacing saturated fat with refined starches or added sugars offers no benefit or increases risk, whereas replacing it with complex whole grains or unsaturated fats is protective."
    },
    {
        "question": "Will closure of a patent foramen ovale (PFO) prevent recurrent stroke in all patients with cryptogenic stroke regardless of anatomical shunt features?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "Clinical trials demonstrate substantial stroke prevention benefits primarily in patients with high-risk anatomical features, such as large shunts or atrial septal aneurysms, whereas the benefit in low-risk or small shunts remains ambiguous."
    },
    {
        "question": "Does taking daily high-dose vitamin D supplements reduce major adverse cardiovascular events in individuals with normal baseline blood vitamin D levels?",
        "answer": "uncertain",
        "specialty": SPECIALTY,
        "explanation": "Large randomized clinical trials like the VITAL trial have found that routine vitamin D supplementation does not reduce the incidence of myocardial infarction, stroke, or cardiovascular mortality in people without baseline deficiency."
    }
]

print(f"New True: {len(NEW_TRUE)}")
print(f"New False: {len(NEW_FALSE)}")
print(f"New Uncertain: {len(NEW_UNCERTAIN)}")
assert len(NEW_TRUE) == 31
assert len(NEW_FALSE) == 32
assert len(NEW_UNCERTAIN) == 12

ALL_QUESTIONS = ORIGINAL_QUESTIONS + NEW_TRUE + NEW_FALSE + NEW_UNCERTAIN
print(f"Total: {len(ALL_QUESTIONS)}")
assert len(ALL_QUESTIONS) == 100

from collections import Counter
counts = Counter(q["answer"] for q in ALL_QUESTIONS)
print("Answer counts:", dict(counts))
assert counts["true"] == 40
assert counts["false"] == 40
assert counts["uncertain"] == 20

# Check uniqueness of question strings (lowercased/stripped)
q_texts = [q["question"].strip().lower() for q in ALL_QUESTIONS]
unique_q_texts = set(q_texts)
print(f"Unique questions: {len(unique_q_texts)}")
assert len(unique_q_texts) == 100, f"Duplicates found: {len(q_texts) - len(unique_q_texts)}"

# Check schema and types
for i, q in enumerate(ALL_QUESTIONS):
    assert "question" in q and isinstance(q["question"], str) and len(q["question"]) > 10, f"Invalid question at index {i}"
    assert "answer" in q and q["answer"] in ["true", "false", "uncertain"], f"Invalid answer at index {i}"
    assert "specialty" in q and q["specialty"] == "Cardiology", f"Invalid specialty at index {i}"
    assert "explanation" in q and isinstance(q["explanation"], str) and len(q["explanation"]) > 20, f"Invalid explanation at index {i}"

print("All assertions passed!")
