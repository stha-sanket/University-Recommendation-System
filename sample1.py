import pandas as pd

# Create a sample dataset
data = pd.DataFrame({
    'University Name': [
        'Harvard University',
        'Stanford University',
        'MIT',
        'University of California, Berkeley',
        'University of Toronto',
        'University of Oxford',
        'University of Cambridge',
        'University of Melbourne',
        'ETH Zurich',
        'National University of Singapore'
    ],
    'Subjects Offered': [
        'Computer Science, Mathematics',
        'Engineering, Business',
        'Engineering, Physics',
        'Social Sciences, Law',
        'Computer Engineering, Arts',
        'Computer Science, Philosophy',
        'Mechanical Engineering, Natural Sciences',
        'Computer Science, Arts',
        'Engineering, Mathematics',
        'Engineering, Business'
    ],
    'IELTS Score': [
        7.5,
        7.0,
        7.5,
        6.5,
        6.5,
        7.0,
        7.5,
        6.5,
        7.0,
        6.5
    ],
    'Country': [
        'USA',
        'USA',
        'USA',
        'USA',
        'Canada',
        'UK',
        'UK',
        'Australia',
        'Switzerland',
        'Singapore'
    ],
    'City': [
        'Cambridge',
        'Stanford',
        'Cambridge',
        'Berkeley',
        'Toronto',
        'Oxford',
        'Cambridge',
        'Melbourne',
        'Zurich',
        'Singapore'
    ],
    'State/Province': [
        'Massachusetts',
        'California',
        'Massachusetts',
        'California',
        'Ontario',
        'England',
        'England',
        'Victoria',
        'Zurich',
        'Singapore'
    ],
    'Tuition Cost': [
        50000,
        55000,
        53000,
        42000,
        32000,
        40000,
        39000,
        45000,
        30000,
        36000
    ],
    'World Ranking': [
        1,
        2,
        3,
        4,
        18,
        5,
        7,
        8,
        9,
        10
    ]
})

class University:
    def __init__(self, name, subjects, ielts, country, city, state, tuition, world_ranking):
        self.name = name
        self.subjects = [s.upper() for s in subjects]  # Store subjects in uppercase
        self.ielts = ielts
        self.country = country.upper()
        self.city = city
        self.state = state
        self.tuition = tuition
        self.world_ranking = world_ranking

class UniversityRanking:
    def __init__(self):
        self.universities = []

    def add_university(self, university):
        self.universities.append(university)

    def filter_universities(self, country=None, max_ielts=None, subject=None):
        filtered = self.universities
        if country:
            filtered = [u for u in filtered if u.country == country]
            if not filtered:
                print(f"No universities found for {country}.")
                return []
        if max_ielts is not None:
            filtered = [u for u in filtered if u.ielts <= max_ielts]
        if subject:
            # Check if any subject in the university subjects matches the user input subject
            filtered = [u for u in filtered if any(subject in subj for subj in u.subjects)]
        return filtered

    def rank_universities(self, universities, top_n=None):
        sorted_universities = sorted(universities, key=lambda x: x.world_ranking)
        return sorted_universities[:top_n] if top_n else sorted_universities

    def display_universities(self, universities):
        if not universities:
            print("No universities match the criteria.")
            return

        data = []
        for uni in universities:
            data.append({
                "University Name": uni.name,
                "Subjects Offered": ', '.join(uni.subjects),
                "World Ranking": uni.world_ranking,
                "IELTS Score": uni.ielts,
                "City": uni.city,
                "State/Province": uni.state,
                "Tuition Cost": f"${uni.tuition:,}"
            })
        df = pd.DataFrame(data)
        print(df.to_string(index=False))

def process_subjects(subject_str):
    return [subject.strip().upper() for subject in subject_str.split(',')]

# Initialize the UniversityRanking system
university_ranking = UniversityRanking()

# Load the dataset into the UniversityRanking system
for index, row in data.iterrows():
    university = University(
        name=row['University Name'],
        subjects=process_subjects(row['Subjects Offered']),
        ielts=row['IELTS Score'],
        country=row['Country'],
        city=row['City'],
        state=row['State/Province'],
        tuition=int(row['Tuition Cost']),
        world_ranking=int(row['World Ranking'])
    )
    university_ranking.add_university(university)

# Main loop for continuous running
while True:
    # User input
    country = input("Enter a country (or press Enter to skip): ").strip().upper()
    max_ielts_input = input("Enter maximum IELTS score (or press Enter to skip): ").strip()
    max_ielts = float(max_ielts_input) if max_ielts_input else None
    subject_input = input("Enter a subject (or press Enter to skip): ").strip().upper()
    subject = subject_input if subject_input else None
    top_n_input = input("Enter the number of universities to display: ")
    top_n = int(top_n_input) if top_n_input.isdigit() else None

    # Filter and rank universities
    filtered_universities = university_ranking.filter_universities(country, max_ielts, subject)
    ranked_universities = university_ranking.rank_universities(filtered_universities, top_n=top_n)

    # Display results
    print(f"\nTop {top_n if top_n else 'all'} universities ranked in {country} by world ranking:")
    university_ranking.display_universities(ranked_universities)

    # Ask if the user wants to continue or exit
    exit_choice = input("\nDo you want to search again? (yes to continue, any other key to exit): ").strip().lower()
    if exit_choice != 'yes':
        print("Exiting the program. Goodbye!")
        break
