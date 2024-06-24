#version 330

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 in_position;

out vec3 frag_position;

void main() {
    gl_Position = projection * view * model * vec4(in_position, 1.0);
    frag_position = vec3(model * vec4(in_position, 1.0));
}
