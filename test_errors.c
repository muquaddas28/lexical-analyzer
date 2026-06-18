/* ============================================
   Sample Program: Lexical Errors Demo
   This file contains intentional errors
   to demonstrate error detection
   ============================================ */

int main() {

    // Valid declarations
    int x = 10;
    float salary = 5500.75;

    // ERROR 1: Unknown token '@' — not a valid character
    int result = x @ 5;

    // ERROR 2: Unterminated string literal — missing closing quote
    char name = "Ali Khan;

    // ERROR 3: Unknown token '#' — not valid outside preprocessor
    int total = x # 3;

    // ERROR 4: Unknown token '$' — not a valid C symbol
    float rate = salary $ 100;

    // Valid code after errors — lexer continues
    int count = 0;
    while (count < 3) {
        count = count + 1;
    }

    return 0;
}
