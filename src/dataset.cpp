#include "dataset.hpp"

#include <fstream>
#include <sstream>
#include <stdexcept>

Dataset loadCsv(const std::string& path)
{
    std::ifstream file(path);
    if (!file)
        throw std::runtime_error("cannot open " + path);

    Dataset     data;
    std::string line;
    while (std::getline(file, line))
    {
        if (line.empty())
            continue;
        std::stringstream   ss(line);
        std::string         cell;
        std::vector<double> row;

        std::getline(ss, cell, ',');
        data.y.push_back(std::stoi(cell));
        while (std::getline(ss, cell, ','))
            row.push_back(std::stod(cell));

        if (!data.X.empty() && row.size() != data.X.front().size())
            throw std::runtime_error("inconsistent column count in " + path);
        data.X.push_back(std::move(row));
    }
    if (data.X.empty())
        throw std::runtime_error("empty dataset: " + path);
    return data;
}
