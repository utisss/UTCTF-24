#include <stdio.h>

void l1(char* s) {
    *s = 'u';
    l2(s + 1);
}

void l2(char* s) {
    *s = 't';
    l3(s + 1);
}

void l3(char* s) {
    *s = 'f';
    l4(s + 1);
}

void l4(char* s) {
    *s = 'l';
    l5(s + 1);
}

void l5(char* s) {
    *s = 'a';
    l6(s + 1);
}

void l6(char* s) {
    *s = 'g';
    l7(s + 1);
}

void l7(char* s) {
    *s = '{';
    l8(s + 1);
}

void l8(char* s) {
    *s = 'i';
    l9(s + 1);
}

void l9(char* s) {
    *s = '_';
    l10(s + 1);
}

void l10(char* s) {
    *s = 'c';
    l11(s + 1);
}

void l11(char* s) {
    *s = '4';
    l12(s + 1);
}

void l12(char* s) {
    *s = 'n';
    l13(s + 1);
}

void l13(char* s) {
    *s = '_';
    l14(s + 1);
}

void l14(char* s) {
    *s = 'r';
    l15(s + 1);
}

void l15(char* s) {
    *s = '3';
    l16(s + 1);
}

void l16(char* s) {
    *s = 'v';
    l17(s + 1);
}

void l17(char* s) {
    *s = '!';
    l18(s + 1);
}

void l18(char* s) {
    *s = '}';
    l19(s + 1);
}

void l19(char* s) {
    *s = '\0';
}   

void keygen() {
    char key[17];
    l1(key);
}

int main() {
    keygen();
    return 0;
}