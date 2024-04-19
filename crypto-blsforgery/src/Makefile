chall: main.cpp
	g++ -std=c++20 -I. -O3 -o forgery main.cpp libbls12-381.a
	strip forgery

solver: solve.cpp
	g++ -std=c++20 -I. -o solver solve.cpp libbls12-381.a