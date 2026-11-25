#include "doctest.h"
#include "dataset.hpp"
#include "test_utils.hpp"

TEST_CASE("loadCsv")
{
    SUBCASE("File not found")
    {
        CHECK_THROWS(loadCsv("does_not_exist.csv"));
    }
    SUBCASE("Wrong extension")
    {
        fs::path path;
        path = fs::temp_directory_path()
               / ("mlp_test_" + std::to_string(std::random_device{}()) + ".bin");
        std::ofstream{path};
        REQUIRE_THROWS_WITH(loadCsv(path), doctest::Contains("extension"));
    }

    SUBCASE("Empty file")
    {
        TmpFile f("");
        REQUIRE_THROWS_WITH(loadCsv(f.path), doctest::Contains("empty"));
    }

    SUBCASE("Wrong file format")
    {
        TmpFile f("something ain't right");
        REQUIRE_THROWS_WITH(loadCsv(f.path), doctest::Contains("stoi"));
    }

    SUBCASE("feature reading")
    {
        TmpFile csv("1,0.5,1.5\n0,2.0,3.0\n");
        Dataset d = loadCsv(csv.path);
        REQUIRE(d.X.size() == 2);   // REQUIRE arrête le test s'il échoue
        CHECK(d.y[0] == 1);
        CHECK(d.y[1] == 0);
        CHECK(d.X[0][0] == doctest::Approx(0.5));
    }
  }