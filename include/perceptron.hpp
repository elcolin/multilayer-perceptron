#pragma once

#include "activation.hpp"

template <typename Activation = Sigmoid>
class Perceptron
{
    private:
    public:
        Perceptron() = default;
        ~Perceptron() = default;

        // double activate(double z) const { return Activation::apply(z); }
        // double activateDerivative(double z) const { return Activation::derivative(z); }
};
