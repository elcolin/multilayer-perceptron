#pragma once

#include "activation.hpp"
#include <vector>
#include <numeric>
#include <stdexcept>

template<typename Activation = Sigmoid>
class Perceptron
{
    private:
        std::vector<double> _weights; // un poids par feature (30)
        double              _bias;

    public:
        explicit Perceptron(std::size_t nInputs) : _weights(nInputs, 0.0), _bias(0.0) 
        {
            if (nInputs == 0)
                throw std::invalid_argument("Perceptron::Perceptron: number of inputs can't be null");
        }

        double forward(const std::vector<double>& x) const 
        {
            if (x.empty())
                throw std::invalid_argument("Perceptron::forward: empty input vector");
            if (x.size() != _weights.size())
                throw std::invalid_argument("Perceptron::forward: wrong size vector");
            double z = std::inner_product(x.begin(), x.end(), _weights.begin(), _bias);
            return Activation{}.apply(z);
        };
};
