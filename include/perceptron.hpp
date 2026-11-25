#pragma once

#include "activation.hpp"
#include <vector>

template<typename Activation = Sigmoid>
class Perceptron
{
    private:
        std::vector<double> _weights; // un poids par feature (30)
        double              _bias;

    public:
        explicit Perceptron(std::size_t nInputs) : _weights(nInputs, 0.0), _bias(0.0) {}

        double forward(const std::vector<double>& x) const { (void) x; return 0;};
};
