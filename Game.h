#pragma once
#include <GLFW/glfw3.h> 

#include "Renderer.h" 

#include "InputHandler.h" 

#include "Skybox.h" 

#include <irrKlang.h> 



class Game {

public:

    Game(GLFWwindow* window);

    ~Game();

    void update();

    void render();



private:

    GLFWwindow* window;

    Renderer* renderer;

    InputHandler* inputHandler;

    Skybox* skybox;

    irrklang::ISoundEngine* 
    soundEngine;

};