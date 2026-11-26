#include "doctest.h"
#include "activation.hpp"

using doctest::Approx;

TEST_CASE("Sigmoid")
{
    struct Sigmoid sig;
    SUBCASE("Apply")
    {
        CHECK(sig.apply(0.0)  == Approx(0.5));
        CHECK(sig.apply(1.0)  == Approx(0.7310585786));
        CHECK(sig.apply(-1.0) == Approx(0.2689414214));
        CHECK(sig.apply(10.0) == Approx(1.0).epsilon(1e-4));
    }
}