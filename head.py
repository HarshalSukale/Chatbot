import spacy

# Load SpaCy model for NLP processing
nlp = spacy.load("en_core_web_sm")

# Define tax laws and deductions (as given previously)
tax_laws = {
    "Section 80C": {
        "description": "Deductions on investments like PPF, EPF, ELSS, etc.",
        "limit": 150000,
        "investments": [
            {"name": "PPF", "description": "Public Provident Fund", "benefit": "Tax-free interest",
             "application_steps": [
                 "Visit a post office or bank where PPF is offered.",
                 "Fill out the PPF account opening form.",
                 "Submit KYC documents and initial deposit."
             ],
             "application_link": "https://www.ppf.gov.in/"},
            {"name": "ELSS", "description": "Equity Linked Savings Scheme", "benefit": "Tax-free returns after 3 years",
             "application_steps": [
                 "Choose a mutual fund company offering ELSS.",
                 "Complete the KYC process with the mutual fund.",
                 "Invest in ELSS through the company’s website or physical branch."
             ],
             "application_link": "https://groww.in/mutual-funds/elss"},
            {"name": "NPS", "description": "National Pension Scheme",
             "benefit": "Additional deduction of Rs 50,000 under section 80CCD(1B)",
             "application_steps": [
                 "Visit the official NPS website or a designated Point of Presence (POP).",
                 "Complete the registration form and KYC process.",
                 "Make your contribution through online or offline modes."
             ],
             "application_link": "https://www.npscra.nsdl.co.in/"},
        ]
    },
    "Section 80D": {
        "description": "Deductions on health insurance premiums",
        "limit": 25000,
        "additional_for_senior_citizens": 50000,
        "investments": [
            {"name": "Health Insurance", "description": "Premium paid for health insurance",
             "benefit": "Deduction based on age group",
             "application_steps": [
                 "Purchase a health insurance policy from an insurance company.",
                 "Ensure the policy is in the name of the insured person.",
                 "Keep the premium receipts for claiming deductions."
             ],
             "application_link": "https://www.policybazaar.com/health-insurance/"},
        ]
    },
    "Section 80E": {
        "description": "Deductions on interest paid on education loans",
        "limit": "No upper limit",
        "investments": [
            {"name": "Education Loan", "description": "Loan taken for higher education",
             "benefit": "Deduction on interest paid",
             "application_steps": [
                 "Apply for an education loan from a bank or financial institution.",
                 "Keep records of loan disbursement and interest payments.",
                 "Claim the deduction while filing your income tax return."
             ],
             "application_link": "https://www.bankbazaar.com/education-loan.html"},
        ]
    }
}

# Define eligibility criteria (as given previously)
eligibility_criteria = {
    "Section 80C": {
        "eligible_person": "Individual and HUF",
        "max_age": "No age limit",
        "income_limit": "No income limit"
    },
    "Section 80D": {
        "eligible_person": "Individual and HUF",
        "max_age": 60,
        "income_limit": "No income limit"
    },
    "Section 80E": {
        "eligible_person": "Individual (for self, spouse, children)",
        "max_age": "No age limit",
        "income_limit": "No income limit"
    }
}

def get_tax_saving_options(income, age):
    applicable_schemes = []
    for section, data in tax_laws.items():
        if section in eligibility_criteria:
            criteria = eligibility_criteria[section]
            max_age = criteria.get("max_age", float('inf'))

            # Ensure max_age is a number before comparison
            if isinstance(max_age, int) or isinstance(max_age, float):
                if age <= max_age:
                    applicable_schemes.append({
                        "section": section,
                        "description": data["description"],
                        "limit": data["limit"],
                        "investments": data["investments"]
                    })
            else:
                # If max_age is not a number, assume no age limit
                applicable_schemes.append({
                    "section": section,
                    "description": data["description"],
                    "limit": data["limit"],
                    "investments": data["investments"]
                })

    return applicable_schemes

def greet_user():
    print("Welcome to the Tax Saving Assistant!")
    print("I can help you find the best tax-saving schemes based on your annual income.")

def get_annual_income():
    try:
        income = float(input("Please enter your annual income (in INR): "))
        return income
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return get_annual_income()

def categorize_income(income):
    if income <= 250000:
        bracket = "No Tax"
    elif 250001 <= income <= 500000:
        bracket = "5% Tax Bracket"
    elif 500001 <= income <= 1000000:
        bracket = "20% Tax Bracket"
    else:
        bracket = "30% Tax Bracket"
    return bracket

def ask_user_for_schemes():
    response = input("Would you like to see tax-saving schemes to reduce your tax liability? (yes/no): ").strip().lower()
    doc = nlp(response)
    for token in doc:
        if token.lemma_ in ['yes', 'yeah', 'yup']:
            return True
        elif token.lemma_ in ['no', 'nope', 'nah']:
            return False
    return False  # Default to 'no' if the response is not clear

def display_tax_saving_schemes(income, age):
    tax_saving_options = get_tax_saving_options(income, age)
    if tax_saving_options:
        print("Here are some tax-saving schemes that you can consider:")
        for idx, option in enumerate(tax_saving_options, start=1):
            print(f"{idx}. Section: {option['section']}")
            print(f"   Description: {option['description']}")
            print(f"   Investment Limit: INR {option['limit']}")

        # Ask user which scheme they want to explore
        scheme_choice = input(
            "Would you like to explore details of any scheme? (Enter the number or 'no' to exit): ").strip().lower()

        if scheme_choice != 'no':
            try:
                choice_idx = int(scheme_choice) - 1
                if 0 <= choice_idx < len(tax_saving_options):
                    selected_option = tax_saving_options[choice_idx]
                    print(f"\nDetailed Information about {selected_option['section']}:")
                    print(f"Description: {selected_option['description']}")
                    print(f"Investment Limit: INR {selected_option['limit']}")
                    for investment in selected_option['investments']:
                        print(f"\nInvestment: {investment['name']}")
                        print(f"Description: {investment['description']}")
                        print(f"Benefit: {investment['benefit']}")
                        print("Application Steps:")
                        for step in investment['application_steps']:
                            print(f"- {step}")
                        print(f"Application Link: {investment['application_link']}")
                else:
                    print("Invalid choice. Please run the program again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("No applicable tax-saving schemes found based on the provided information.")

def main():
    # Step 1: Greet the user
    greet_user()

    # Step 2: Ask for annual income
    income = get_annual_income()

    # Step 3: Categorize the user into a tax bracket
    tax_bracket = categorize_income(income)
    print(f"Based on your income of INR {income}, you fall under the '{tax_bracket}'.")

    # Step 4: Ask the user if they want to see tax-saving schemes
    see_schemes = ask_user_for_schemes()

    if see_schemes:
        age = int(input("Please enter your age: "))  # Ask the user's age
        display_tax_saving_schemes(income, age)
    else:
        print("Thank you for using the Tax Saving Assistant!")

if _name_ == "_main_":
    main()
import spacy

# Load SpaCy model for NLP processing
nlp = spacy.load("en_core_web_sm")

# Define tax laws and deductions (as given previously)
tax_laws = {
    "Section 80C": {
        "description": "Deductions on investments like PPF, EPF, ELSS, etc.",
        "limit": 150000,
        "investments": [
            {"name": "PPF", "description": "Public Provident Fund", "benefit": "Tax-free interest",
             "application_steps": [
                 "Visit a post office or bank where PPF is offered.",
                 "Fill out the PPF account opening form.",
                 "Submit KYC documents and initial deposit."
             ],
             "application_link": "https://www.ppf.gov.in/"},
            {"name": "ELSS", "description": "Equity Linked Savings Scheme", "benefit": "Tax-free returns after 3 years",
             "application_steps": [
                 "Choose a mutual fund company offering ELSS.",
                 "Complete the KYC process with the mutual fund.",
                 "Invest in ELSS through the company’s website or physical branch."
             ],
             "application_link": "https://groww.in/mutual-funds/elss"},
            {"name": "NPS", "description": "National Pension Scheme",
             "benefit": "Additional deduction of Rs 50,000 under section 80CCD(1B)",
             "application_steps": [
                 "Visit the official NPS website or a designated Point of Presence (POP).",
                 "Complete the registration form and KYC process.",
                 "Make your contribution through online or offline modes."
             ],
             "application_link": "https://www.npscra.nsdl.co.in/"},
        ]
    },
    "Section 80D": {
        "description": "Deductions on health insurance premiums",
        "limit": 25000,
        "additional_for_senior_citizens": 50000,
        "investments": [
            {"name": "Health Insurance", "description": "Premium paid for health insurance",
             "benefit": "Deduction based on age group",
             "application_steps": [
                 "Purchase a health insurance policy from an insurance company.",
                 "Ensure the policy is in the name of the insured person.",
                 "Keep the premium receipts for claiming deductions."
             ],
             "application_link": "https://www.policybazaar.com/health-insurance/"},
        ]
    },
    "Section 80E": {
        "description": "Deductions on interest paid on education loans",
        "limit": "No upper limit",
        "investments": [
            {"name": "Education Loan", "description": "Loan taken for higher education",
             "benefit": "Deduction on interest paid",
             "application_steps": [
                 "Apply for an education loan from a bank or financial institution.",
                 "Keep records of loan disbursement and interest payments.",
                 "Claim the deduction while filing your income tax return."
             ],
             "application_link": "https://www.bankbazaar.com/education-loan.html"},
        ]
    }
}

# Define eligibility criteria (as given previously)
eligibility_criteria = {
    "Section 80C": {
        "eligible_person": "Individual and HUF",
        "max_age": "No age limit",
        "income_limit": "No income limit"
    },
    "Section 80D": {
        "eligible_person": "Individual and HUF",
        "max_age": 60,
        "income_limit": "No income limit"
    },
    "Section 80E": {
        "eligible_person": "Individual (for self, spouse, children)",
        "max_age": "No age limit",
        "income_limit": "No income limit"
    }
}

def get_tax_saving_options(income, age):
    applicable_schemes = []
    for section, data in tax_laws.items():
        if section in eligibility_criteria:
            criteria = eligibility_criteria[section]
            max_age = criteria.get("max_age", float('inf'))

            # Ensure max_age is a number before comparison
            if isinstance(max_age, int) or isinstance(max_age, float):
                if age <= max_age:
                    applicable_schemes.append({
                        "section": section,
                        "description": data["description"],
                        "limit": data["limit"],
                        "investments": data["investments"]
                    })
            else:
                # If max_age is not a number, assume no age limit
                applicable_schemes.append({
                    "section": section,
                    "description": data["description"],
                    "limit": data["limit"],
                    "investments": data["investments"]
                })

    return applicable_schemes

def greet_user():
    print("Welcome to the Tax Saving Assistant!")
    print("I can help you find the best tax-saving schemes based on your annual income.")

def get_annual_income():
    try:
        income = float(input("Please enter your annual income (in INR): "))
        return income
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return get_annual_income()

def categorize_income(income):
    if income <= 250000:
        bracket = "No Tax"
    elif 250001 <= income <= 500000:
        bracket = "5% Tax Bracket"
    elif 500001 <= income <= 1000000:
        bracket = "20% Tax Bracket"
    else:
        bracket = "30% Tax Bracket"
    return bracket

def ask_user_for_schemes():
    response = input("Would you like to see tax-saving schemes to reduce your tax liability? (yes/no): ").strip().lower()
    doc = nlp(response)
    for token in doc:
        if token.lemma_ in ['yes', 'yeah', 'yup']:
            return True
        elif token.lemma_ in ['no', 'nope', 'nah']:
            return False
    return False  # Default to 'no' if the response is not clear

def display_tax_saving_schemes(income, age):
    tax_saving_options = get_tax_saving_options(income, age)
    if tax_saving_options:
        print("Here are some tax-saving schemes that you can consider:")
        for idx, option in enumerate(tax_saving_options, start=1):
            print(f"{idx}. Section: {option['section']}")
            print(f"   Description: {option['description']}")
            print(f"   Investment Limit: INR {option['limit']}")

        # Ask user which scheme they want to explore
        scheme_choice = input(
            "Would you like to explore details of any scheme? (Enter the number or 'no' to exit): ").strip().lower()

        if scheme_choice != 'no':
            try:
                choice_idx = int(scheme_choice) - 1
                if 0 <= choice_idx < len(tax_saving_options):
                    selected_option = tax_saving_options[choice_idx]
                    print(f"\nDetailed Information about {selected_option['section']}:")
                    print(f"Description: {selected_option['description']}")
                    print(f"Investment Limit: INR {selected_option['limit']}")
                    for investment in selected_option['investments']:
                        print(f"\nInvestment: {investment['name']}")
                        print(f"Description: {investment['description']}")
                        print(f"Benefit: {investment['benefit']}")
                        print("Application Steps:")
                        for step in investment['application_steps']:
                            print(f"- {step}")
                        print(f"Application Link: {investment['application_link']}")
                else:
                    print("Invalid choice. Please run the program again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("No applicable tax-saving schemes found based on the provided information.")

def main():
    # Step 1: Greet the user
    greet_user()

    # Step 2: Ask for annual income
    income = get_annual_income()

    # Step 3: Categorize the user into a tax bracket
    tax_bracket = categorize_income(income)
    print(f"Based on your income of INR {income}, you fall under the '{tax_bracket}'.")

    # Step 4: Ask the user if they want to see tax-saving schemes
    see_schemes = ask_user_for_schemes()

    if see_schemes:
        age = int(input("Please enter your age: "))  # Ask the user's age
        display_tax_saving_schemes(income, age)
    else:
        print("Thank you for using the Tax Saving Assistant!")

if __name__ == "__main__":
    main()
