#include <vector>
#include <string>
#include <GL/glew.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include "CGLSLProgram.h" // Suponiendo que CGLSLProgram es una clase que maneja programas GLSL
#include "stb_image.h"    // Para cargar imágenes

class skyBox {
public:
    skyBox(const std::vector<std::string>& faces, CGLSLProgram* glslSkyBox)
        : glslSkyBox(glslSkyBox), faces(faces) {
        init();
    }

    void display(glm::mat4 view, glm::mat4 projection) {
        glslSkyBox->enable();

        // Elimina la parte de translación de la matriz de vista
        view = glm::mat4(glm::mat3(view));

        glslSkyBox->loadUniformMatrix("projection", GShader::UNIFORM_SIZE_4D, glm::value_ptr(projection));
        glslSkyBox->loadUniformMatrix("view", GShader::UNIFORM_SIZE_4D, glm::value_ptr(view));

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
        glDepthFunc(GL_LEQUAL);

        glBindVertexArray(skyboxVAO);
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_CUBE_MAP, cubemapTexture);
        glDrawArrays(GL_TRIANGLES, 0, 36);
        glBindVertexArray(0);

        glDepthFunc(GL_LESS);

        glslSkyBox->disable();
    }

private:
    unsigned int loadCubemap(const std::vector<std::string>& faces) {
        unsigned int textureID;
        glGenTextures(1, &textureID);
        glBindTexture(GL_TEXTURE_CUBE_MAP, textureID);

        int width, height, nrChannels;
        for (unsigned int i = 0; i < faces.size(); ++i) {
            unsigned char* data = stbi_load(faces[i].c_str(), &width, &height, &nrChannels, 0);
            if (data) {
                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
                stbi_image_free(data);
            }
            else {
                printf("Failed to load cubemap texture at path: %s\n", faces[i].c_str());
                stbi_image_free(data);
                return 0; // or handle error as needed
            }
        }
        // Set cubemap texture parameters

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE);

        return textureID;
    }

    void init() {
        // Skybox vertices scaled to maintain aspect ratio suitable for a 920x690 screen
        float skyboxVertices[] = {
            // Positions
            // Front face
            -1.0f,  1.0f, -1.0f,
            -1.0f, -1.0f, -1.0f,
             1.0f, -1.0f, -1.0f,
             1.0f, -1.0f, -1.0f,
             1.0f,  1.0f, -1.0f,
            -1.0f,  1.0f, -1.0f,

            // Left face
            -1.0f, -1.0f,  1.0f,
            -1.0f, -1.0f, -1.0f,
            -1.0f,  1.0f, -1.0f,
            -1.0f,  1.0f, -1.0f,
            -1.0f,  1.0f,  1.0f,
            -1.0f, -1.0f,  1.0f,

            // Right face
             1.0f, -1.0f, -1.0f,
             1.0f, -1.0f,  1.0f,
             1.0f,  1.0f,  1.0f,
             1.0f,  1.0f,  1.0f,
             1.0f,  1.0f, -1.0f,
             1.0f, -1.0f, -1.0f,

             // Back face
             -1.0f, -1.0f,  1.0f,
             -1.0f,  1.0f,  1.0f,
              1.0f,  1.0f,  1.0f,
              1.0f,  1.0f,  1.0f,
              1.0f, -1.0f,  1.0f,
             -1.0f, -1.0f,  1.0f,

             // Top face
             -1.0f,  1.0f, -1.0f,
              1.0f,  1.0f, -1.0f,
              1.0f,  1.0f,  1.0f,
              1.0f,  1.0f,  1.0f,
             -1.0f,  1.0f,  1.0f,
             -1.0f,  1.0f, -1.0f,

             // Bottom face
             -1.0f, -1.0f, -1.0f,
             -1.0f, -1.0f,  1.0f,
              1.0f, -1.0f, -1.0f,
              1.0f, -1.0f, -1.0f,
             -1.0f, -1.0f,  1.0f,
              1.0f, -1.0f,  1.0f
        };

        glGenVertexArrays(1, &skyboxVAO);
        glGenBuffers(1, &skyboxVBO);

        glBindVertexArray(skyboxVAO);
        glBindBuffer(GL_ARRAY_BUFFER, skyboxVBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(skyboxVertices), &skyboxVertices, GL_STATIC_DRAW);
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);

        cubemapTexture = loadCubemap(faces);
    }

private:
    unsigned int skyboxVAO, skyboxVBO;
    unsigned int cubemapTexture;
    std::vector<std::string> faces;
    CGLSLProgram* glslSkyBox; // Suponiendo que CGLSLProgram es una clase que maneja programas GLSL
};