#include "plant.h"

#include <cmath>
#include <vector>
#include <iostream>

using std::vector;
using namespace std;

int
main(int argc, char* argv[]) {
    // Инициализация ОУ.
    Plant plant;
    plant_init(plant);

    // Получение экспериментальных данных.
    const int channel = 64;
    const size_t steps = 100;

    vector<double> xs(steps);
    vector<double> ys(steps);

    for (size_t i = 0; i < steps; i++) {
        xs[i] = i;
        ys[i] = plant_measure(channel, plant);
    }

    for (size_t i = 0; i < steps; i++) {
        cout << ys[i] << '\t'; // Печать экспериментальных данных.
    }

    return 0;
}
