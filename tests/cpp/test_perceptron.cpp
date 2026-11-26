#include "doctest.h"
#include "perceptron.hpp"

TEST_CASE("Constructor")
{
    SUBCASE("Input number equals 0")
    {
        CHECK_THROWS_WITH(Perceptron(0), doctest::Contains("null"));
    }
}

using doctest::Approx;

TEST_CASE("forward")
{
    Perceptron<>        p(3);          // setup refait pour chaque SUBCASE
    std::vector<double> x{1.0, 2.0, 3.0};
    SUBCASE("Empty vector")
    {
        std::vector<double> e;
        CHECK_THROWS_WITH(p.forward(e), doctest::Contains("empty"));
    }
    SUBCASE("Wrong size vector")
    {
        std::vector<double> s{1.0};
        CHECK_THROWS_WITH(p.forward(s), doctest::Contains("size"));
    }
    SUBCASE("Forward")
    {
        CHECK(p.forward(x) == Approx(0.5));
    }
}