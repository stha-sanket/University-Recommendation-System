import pandas as pd
from collections import defaultdict

# Load the dataset
df = pd.read_csv('DSA_university_dataset.csv', encoding='ISO-8859-1')

# Step 1: Build Trie for subject matching
class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# Step 2: Build Trie from subjects offered
subject_trie = Trie()
for subject in df['Subjects Offered']:
    for sub in subject.split(", "):  # Handle multiple subjects in a cell
        subject_trie.insert(sub.strip().upper())

# Step 3: Filter function using binary search for world ranking and Trie for subject matching
def filter_universities(df):
    df_sorted = df.sort_values(by='World Ranking')  # Sorting by World Ranking

    while True:
        # Get user inputs
        country = input("Enter the country: ").strip().lower()
        ielts = float(input("Enter your IELTS score: "))
        subject = input("Enter the subject category (e.g., Engineering): ").strip().upper()
        n = int(input("Enter the number of universities to display: "))

        # Step 4: Filter by country and IELTS score
        filtered_df = df_sorted[
            (df_sorted['Country'].str.lower() == country) &
            (df_sorted['IELTS Score'] <= ielts)
        ]

        # Step 5: Filter using the Trie for subjects
        subject_filtered_df = filtered_df[filtered_df['Subjects Offered'].apply(
            lambda x: any(subject_trie.search(s.strip().upper()) for s in x.split(", "))
        )]

        # Step 6: Display the top N universities
        result = subject_filtered_df.head(n)

        if not result.empty:
            display_columns = ['University Name', 'Subjects Offered', 'World Ranking', 'IELTS Score', 'City', 'State/Province', 'Tuition Cost']
            print(result[display_columns].to_string(index=False))
        else:
            print("No universities found matching the criteria.")

        # Ask if the user wants to continue
        cont = input("Do you want to search again? (yes/no): ").strip().lower()
        if cont == 'no':
            break

# Example usage in your report
filter_universities(df)
