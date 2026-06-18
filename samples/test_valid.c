/* ============================================
   Sample Program: Valid C Code
   Tests all token types in the lexer
   ============================================ */

#include <stdio.h>

int globalCounter = 0;

// Function to calculate factorial
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

float average(int a, int b, int c) {
    float sum = a + b + c;
    return sum / 3;
}

int main() {
    int x = 10;
    int y = 20;
    float result = 0.0;
    bool found = false;
    char grade = 'A';

    /* Loop to demonstrate while and operators */
    int count = 0;
    while (count < 5) {
        count = count + 1;
        globalCounter = globalCounter + 1;
    }

    /* Demonstrate bitwise and logical operators */
    int flags = 0xFF;
    int mask  = flags & 0x0F;
    int shifted = mask << 2;

    if (x > 0 && y != 0) {
        result = average(x, y, count);
        found = true;
    }

    /* Demonstrate switch-case */
    switch (count) {
        case 5:
            grade = 'A';
            break;
        case 3:
            grade = 'B';
            break;
        default:
            grade = 'C';
            break;
    }

    /* For loop */
    for (int i = 0; i < 10; i = i + 1) {
        if (i == 5) {
            continue;
        }
    }

    int fact = factorial(5);
    return 0;
}
