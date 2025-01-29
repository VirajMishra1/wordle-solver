# Import required libraries
import math  # For entropy calculations
from collections import defaultdict  # For efficient counting
from tqdm import tqdm  # For progress bars

class WordleSolver:
    _pattern_cache = {}  # Class-level cache for pattern calculation results
    
    def __init__(self, answer_path, guess_path=None):
        # Initialize with answer words and allowed guesses
        self.answers = self.load_valid_words(answer_path)
        self.allowed = self.load_valid_words(guess_path) if guess_path else self.answers.copy()
        
        # Print loading statistics
        print(f"Loaded {len(self.answers)} answer words")
        print(f"Loaded {len(self.allowed)} allowed guesses")
        
        # Initialize game state
        self.state = {
            'possible': self.answers.copy(),  # Remaining possible solutions
            'correct': ['?'] * 5,  # Known correct letters/positions
            'present': set(),  # Letters that exist in word but position unknown
            'absent': set()  # Letters confirmed not in word
        }

    def load_valid_words(self, file_path):
        # Load and validate 5-letter words from file
        try:
            with open(file_path, 'r') as f:
                # Read and sanitize words
                words = [word.strip().upper() for word in f if len(word.strip()) == 5]
                if not words:
                    raise ValueError(f"No valid 5-letter words found in '{file_path}'!")
                return words
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found!")

    @staticmethod
    def get_pattern(guess, target):
        # Calculate Wordle feedback pattern (C=Correct, P=Present, A=Absent)
        pattern = [''] * 5
        counts = defaultdict(int)
        
        # First pass: Mark correct letters
        for i, (g, t) in enumerate(zip(guess, target)):
            if g == t:
                pattern[i] = 'C'
                counts[t] += 1
        
        # Second pass: Handle present/absent letters
        for i, g in enumerate(guess):
            if pattern[i] == 'C':
                continue
            
            # Calculate available slots for present letters
            total_in_target = sum(1 for t in target if t == g)
            if total_in_target > counts[g]:
                pattern[i] = 'P'
                counts[g] += 1
            else:
                pattern[i] = 'A'
        
        return tuple(pattern)

    @staticmethod
    def get_pattern_cached(guess, target):
        # Memoized version of get_pattern for performance
        key = (guess, target)
        if key not in WordleSolver._pattern_cache:
            WordleSolver._pattern_cache[key] = WordleSolver.get_pattern(guess, target)
        return WordleSolver._pattern_cache[key]

    def calculate_entropy(self, word):
        # Calculate information entropy for a potential guess
        pattern_counts = defaultdict(int)
        # Count patterns for all possible answers
        for possible in self.state['possible']:
            pattern = self.get_pattern_cached(word, possible)
            pattern_counts[pattern] += 1
        
        # Calculate entropy using Shannon's formula
        total = len(self.state['possible'])
        entropy = sum(-(count/total) * math.log2(count/total) 
                      for count in pattern_counts.values())
        return entropy

    def get_best_guess(self):
        # Determine optimal guess using entropy maximization
        best_word = None
        best_score = -float('inf')
        
        print("\nCalculating best initial guess...")
        # Use first 2315 words (standard Wordle answer list size)
        candidates = self.allowed[:2315]
        for word in tqdm(candidates, desc="Analyzing words"):
            score = self.calculate_entropy(word)
            if score > best_score:
                best_score = score
                best_word = word
                tqdm.write(f"Current best: {word} ({score:.2f})")  
        
        return best_word

    def update_state(self, guess, feedback):
        # Update game state based on feedback
        new_possible = []
        
        # Process feedback to update constraints
        for i, (letter, color) in enumerate(feedback):
            if color == 'C':
                self.state['correct'][i] = letter
                if letter in self.state['present']:
                    self.state['present'].remove(letter)
            elif color == 'P':
                self.state['present'].add(letter)
            elif color == 'A':
                self.state['absent'].add(letter)
        
        self.clean_constraints()
        
        # Filter possible words using updated constraints
        for word in self.state['possible']:
            if self.is_word_valid(word):
                new_possible.append(word)
        
        self.state['possible'] = new_possible

    def is_word_valid(self, word):
        # Check if word matches all current constraints
        # Verify correct positions
        for i, c in enumerate(self.state['correct']):
            if c != '?' and word[i] != c:
                return False
        
        # Check required present letters
        if any(p not in word for p in self.state['present']):
            return False
        
        # Check excluded letters
        if any(a in word for a in self.state['absent'] 
               if a not in self.state['correct'] and a not in self.state['present']):
            return False
        
        # Prevent present letters in known incorrect positions
        for i, letter in enumerate(word):
            if letter in self.state['present'] and letter == self.state['correct'][i]:
                return False
        
        return True

    def clean_constraints(self):
        # Remove redundant constraints
        self.state['present'] = {p for p in self.state['present'] if p not in self.state['correct']}
        self.state['absent'] = {a for a in self.state['absent'] 
                                if a not in self.state['correct'] and a not in self.state['present']}

    def print_status(self):
        # Display current game state
        print("\nCurrent Game Status:")
        status = f"Possible words: {len(self.state['possible']):4}"
        if len(self.state['possible']) <= 3:
            status += f" ({', '.join(self.state['possible'])})"
        print(status)

def get_feedback_input(guess):
    # Get and validate user feedback input
    while True:
        print(f"\n{' INPUT REQUIRED ':~^60}")
        print(f"Current Guess: {guess}")
        print("Enter feedback using C/P/A for each letter:")
        print("Example: CPAAP or C P A A P")
        print("(C=Correct, P=Present, A=Absent)")
        print(f"{'-'*60}")
        
        fb = input(">>> Feedback for this guess: ").upper().replace(" ", "")
        
        # Validate input format
        if len(fb) == 5 and all(c in 'CPA' for c in fb):
            return list(zip(guess, fb))
        print("Invalid input! Please use exactly 5 characters (C/P/A)")

def main():
    # Initialize solver with word lists
    solver = WordleSolver(
        answer_path="filepath",
        guess_path="filepath"
    )
    
    # Print welcome banner
    print("\n" + "=" * 60)
    print(" WORDLE SOLVER ".center(60, '='))
    print("=" * 60)
    
    # Main game loop (max 5 attempts)
    for attempt in range(5):
        print(f"\n{' ATTEMPT ' + str(attempt+1) + ' ':=^60}")
        solver.print_status()
        
        # Get and display best guess
        best_guess = solver.get_best_guess()
        if not best_guess:
            print("\nNO MORE POSSIBLE WORDS!")
            break
        
        print(f"\nNEXT GUESS: {best_guess}")
        print("Enter this word in Wordle, then provide feedback:")
        
        # Process feedback and update state
        feedback = get_feedback_input(best_guess)
        solver.update_state(best_guess, feedback)
        
        # Check for win condition
        if len(solver.state['possible']) == 1:
            print(f"\nCONGRATULATIONS! THE WORD IS {solver.state['possible'][0]}!")
            break

if __name__ == "__main__":
    main()