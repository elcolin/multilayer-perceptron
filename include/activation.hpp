#pragma once

#include <cmath>

// Une fonction d'activation = une struct avec deux fonctions statiques :
//   - apply(z)      : f(z)
//   - derivative(z) : f'(z), utile pour la descente de gradient
// Pour en creer une nouvelle, il suffit d'ecrire une struct avec ces deux methodes.

struct Sigmoid
{
    // static double apply(double z) {}
    // static double derivative(double z)
    // {
    // }
};

struct Step
{
};

struct Tanh
{
    // static double apply(double z) {}
    // static double derivative(double z)
    // {
    // }
};

struct ReLU
{
};
