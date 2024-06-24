#pragma once

#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <glm/glm.hpp>

using namespace std;

class Jugador {
public:
    string nombre;
    vector<string> titulos;
    vector<glm::vec3> titulos_colores;
    int titulo_actual;
    vector<int> intentos;
    vector<int> pistas_usadas;
    vector<int> luz_usada;

    Jugador(string nombre);
    Jugador(int a, string nombre); // Este constructor está incompleto en tu código original
    ~Jugador();

    bool load_data(string file);
    void save_data();
    void cambiar_titulo();
    void asignar_titulo(string aux);
};