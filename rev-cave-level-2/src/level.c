#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

//#define JBDEBUG

typedef signed char byte;

typedef struct {
    int type;
    int x;
    int y;
    int d;
} sprite;

#define SPRITE_MARIO 1
#define SPRITE_BADDIE 2

#ifdef JBDEBUG
// Test helpers
char log_buf[1024];
int log_len = 0;
#endif

// Original
#define LEVEL_WIDTH 50
#define LEVEL_HEIGHT 15
#define JUMP_HEIGHT 3

#define BLOCK(bx1, by1, bx2, by2) if (x >= bx1 - dx && x <= bx2 - dx && y >= by1 - dy && y <= by2 - dy) return true;

__attribute__((always_inline)) static bool blocked(int x, int y, int dx, int dy) {
    BLOCK(-1, 0, -1, LEVEL_HEIGHT)
    BLOCK(LEVEL_WIDTH, 0, LEVEL_WIDTH, LEVEL_HEIGHT)
    BLOCK(0, LEVEL_HEIGHT - 1, 19, LEVEL_HEIGHT - 1)
    BLOCK(8, 11, 13, 11)
    BLOCK(17, 10, 24, 10)
    BLOCK(12, 8, 16, 8)
    BLOCK(20, 10, 20, LEVEL_HEIGHT - 1)
    BLOCK(23, 14, 23, 14)
    BLOCK(27, 11, 34, 11)
    BLOCK(37, 8, 37, 8)
    BLOCK(33, 6, 33, 6)
    BLOCK(27, 6, 29, 6)
    return false;
}

sprite sprites[] = {
    { .type = SPRITE_MARIO, .x = 2, .y = 13, .d = 0 },
    { .type = SPRITE_BADDIE, .x = 13, .y = 10, .d = 0 },
    { .type = SPRITE_BADDIE, .x = 15, .y = 13, .d = 0 },
    { .type = SPRITE_BADDIE, .x = 15, .y = 7, .d = 1 },
    { .type = SPRITE_BADDIE, .x = 19, .y = 9, .d = 1 },
    { .type = SPRITE_BADDIE, .x = 23, .y = 13, .d = 1 },
    { .type = SPRITE_BADDIE, .x = 29, .y = 5, .d = 0 },
};

__attribute__((always_inline)) static sprite *at_space(int x, int y) {
    for (int i = 0; i < sizeof(sprites) / sizeof(sprite); i++) {
        if (sprites[i].x == x && sprites[i].y == y) {
            return &sprites[i];
        }
    }
    return 0;
}

#ifdef JBDEBUG
static void debug_draw() {
    for (int y = 0; y < LEVEL_HEIGHT; y++) {
        for (int x = 0; x < LEVEL_WIDTH; x++) {
            if (blocked(x, y, 0, 0)) {
                putc('#', stdout);
            } else {
                sprite *other = at_space(x, y);
                if (other) {
                    if (other->type == SPRITE_MARIO) {
                        putc('M', stdout);
                    } else if (other->type == SPRITE_BADDIE) {
                        putc('R', stdout);
                    } else {
                        putc('?', stdout);
                    }
                } else {
                    putc(' ', stdout);
                }
            }
        }
        putc('\n', stdout);
    }
    fflush(stdout);
}
#endif

__attribute__((always_inline)) static void move(sprite *s, int dx, int dy) {
    if (blocked(s->x, s->y, dx, dy)) return;
    if (s->type == SPRITE_MARIO) {
        if (s->y + dy >= LEVEL_HEIGHT) {
            puts("Game Over");
            exit(1);
        }
    }
    sprite *other;
    sprites:
    other = at_space(s->x + dx, s->y + dy);
    if (other) {
        if (s->type == SPRITE_MARIO) {
            if (dy > 0) {
                other->y = 100;
                other->d = 2;
                // Could have overlap; re-check
                goto sprites;
            } else {
                puts("Game Over");
                exit(1);
            }
        }
        if (other->type == SPRITE_MARIO) {
            puts("Game Over");
            exit(1);
        }
    }
    s->x += dx;
    s->y += dy;
}

int main() {
    puts("Welcome to my game");
    while (true) {
        bool won = 1;
        for (int i = 0; i < sizeof(sprites) / sizeof(sprite); i++) {
            if (sprites[i].type == SPRITE_MARIO) {
                #ifdef JBDEBUG
                debug_draw();
                #endif
                int dir = getc(stdin);
                while (dir == '\n') {
                    dir = getc(stdin);
                }
                if (dir < 0) {
                    exit(1);
                }
                #ifdef JBDEBUG
                if (log_len < sizeof(log_buf) - 1) {
                    log_buf[log_len++] = dir;
                }
                #endif
                if (dir == 'a' && !blocked(sprites[i].x, sprites[i].y, -1, 0)) {
                    move(&sprites[i], -1, 0);
                } else if (dir == 'd' && !blocked(sprites[i].x, sprites[i].y, 1, 0)) {
                    move(&sprites[i], 1, 0);
                } else if (dir == 'w' && blocked(sprites[i].x, sprites[i].y, 0, 1)) {
                    sprites[i].d = JUMP_HEIGHT;
                }
                if (sprites[i].d > 0 && !blocked(sprites[i].x, sprites[i].y, 0, -1)) {
                    sprites[i].d--;
                    move(&sprites[i], 0, -1);
                } else {
                    sprites[i].d = 0;
                    if (!blocked(sprites[i].x, sprites[i].y, 0, 1)) {
                        move(&sprites[i], 0, 1);
                    }
                }
            } else if (sprites[i].type == SPRITE_BADDIE) {
                bool left_open = !blocked(sprites[i].x, sprites[i].y, -1, 0) && blocked(sprites[i].x, sprites[i].y, -1, 1);
                bool right_open = !blocked(sprites[i].x, sprites[i].y, 1, 0) && blocked(sprites[i].x, sprites[i].y, 1, 1);
                if (sprites[i].d == 1) {
                    if (right_open) {
                        move(&sprites[i], 1, 0);
                    } else {
                        sprites[i].d = 0;
                        if (left_open) move(&sprites[i], -1, 0);
                    }
                } else if (sprites[i].d == 0) {
                    if (left_open) {
                        move(&sprites[i], -1, 0);
                    } else {
                        sprites[i].d = 1;
                        if (right_open) move(&sprites[i], 1, 0);
                    }
                }
                if (sprites[i].d < 2 && !blocked(sprites[i].x, sprites[i].y, 0, 1)) move(&sprites[i], 0, 1);
            }
            if (sprites[i].type != SPRITE_MARIO && sprites[i].d != 2) {
                won = 0;
            }
        }
        if (won) {
            puts("Level Clear!");
            #ifdef JBDEBUG
            fputs("Log: \"", stdout);
            log_buf[log_len] = '\0';
            fputs(log_buf, stdout);
            fputs("\"\n", stdout);
            fflush(stdout);
            #endif
            system("/bin/cat flag.txt");
            exit(0);
        }
    }
    return 0;
}