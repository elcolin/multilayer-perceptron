#pragma once

#include <string>
#include <vector>

struct Dataset
{
    std::vector<std::vector<double>> X; // features
    std::vector<int>                 y; // labels (0 = B, 1 = M)
};

Dataset loadCsv(const std::string& path);
