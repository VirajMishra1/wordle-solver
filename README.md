# Wordle Solver - Entropy-Based Assistant 🧩

## Project Description

The **Wordle Solver** is a Python-based tool designed to assist players in solving Wordle puzzles efficiently. By leveraging entropy calculations and dynamic state management, the solver recommends optimal guesses based on real-time feedback (Correct, Present, Absent letters). It filters possible words from predefined lists and iteratively narrows down solutions, maximizing the chances of solving the puzzle within fewer attempts.

## 🚀 Features

1. **Entropy-Driven Guesses**: Calculates word entropy to prioritize guesses that maximize information gain.
2. **Dynamic State Updates**: Adjusts possible solutions based on user feedback (C/P/A for each letter).
3. **Word List Management**: Loads valid answer and guess words from text files.
4. **Interactive CLI**: Guides users through inputting feedback and displays progress.
5. **Smart Filtering**: Excludes invalid words using constraints from feedback.
6. **Progress Tracking**: Shows remaining possible words and highlights top candidates.

## 🛠️ Technologies Used

- **Python**: Core programming language.
- **tqdm**: For progress bars during entropy calculations.
- **Defaultdict**: Efficiently manage pattern caching and word lists.

## 📦 Setup and Installation

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    ```
2. **Navigate to the Project Directory**:
    ```bash
    cd wordle-solver
    ```
3. **Install Dependencies**:
    ```bash
    pip install tqdm
    ```
4. **Prepare Word Lists**:
   - Obtain two text files:
     - `wordle_answers.txt`: List of valid answer words (one 5-letter word per line).
     - `wordle_guesses.txt`: List of allowed guess words (optional; if omitted, answers are used).
   - Update the file paths in the `main()` function:
     ```python
     answer_path="/path/to/your/wordle_answers.txt"
     guess_path="/path/to/your/wordle_guesses.txt"
     ```

5. **Run the Solver**:
    ```bash
    python wordle_solver.py
    ```

## 📝 Usage

1. **Start the Solver**:
   - The tool will load word lists and display the number of possible answers/allowed guesses.

2. **Follow Interactive Prompts**:
   - Enter feedback (C/P/A) after each guess. Example: `CPAAP` or `C P A A P`.
   - The solver updates possible words and recommends the next best guess.

3. **Continue Until Solved**:
   - The tool narrows down possibilities and announces the solution when only one word remains.

## 🛡️ Notes

- **Word Lists**: Ensure your answer/guess files contain valid 5-letter words. Public Wordle word lists can be found online.
- **Custom Paths**: Modify `answer_path` and `guess_path` in the script to match your file locations.

## 🤝 Contribution

Contributions are welcome! Improvements to entropy algorithms, efficiency, or UI enhancements are encouraged. Fork the repository and submit a pull request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Viraj Mishra
