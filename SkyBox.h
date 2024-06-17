#pragma once

#include <vector>
#include <string>
#include <GL/glew.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>
#include "CGLSLProgram.h" // Suponiendo que CGLSLProgram es una clase que maneja programas GLSL
#include "stb_image.h"    // Para cargar imágenes

class skyBox {
private:
    unsigned int skyboxVAO, skyboxVBO;
    unsigned int cubemapTexture;
    std::vector<std::string> faces;
    CGLSLProgram* glslSkyBox;

public:
    skyBox(const std::vector<std::string>& faces, CGLSLProgram* glslSkyBox);
    void init();
    void display(glm::mat4 view, glm::mat4 projection);
    unsigned int loadCubemap(const std::vector<std::string>& faces);
    void change_texture(const std::vector<std::string>& faces);
};