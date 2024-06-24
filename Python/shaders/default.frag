#version 330

uniform sampler2D tex;  // Nueva variable uniforme para la textura

in vec3 frag_position;

out vec4 frag_color;

void main() {
    frag_color = texture(tex, frag_position.xy);
}
