$input vWorldPos, vNormal, vTexCoord0, vTexCoord1, vTangent, vBinormal

#include <forward_pipeline.sh>

// Surface attributes
uniform vec4 uDiffuseColor;

// Texture slots
SAMPLER2D(uReflectionMap, 7);

// Entry point of the forward pipeline default uber shader (Phong and PBR)
void main() {
	// vec3 color = uDiffuseColor.xyz;

	vec3 P = vWorldPos; // fragment world pos
	vec3 nv = normalize(vNormal).xyz;
	vec3 V = normalize(GetT(u_invView) - P); // view vector
	vec3 N = normalize(vNormal);
	vec3 R = reflect(-V, N);
	// color *= texture2D(uReflectionMap, R.xy).xyz;

	// vec4 frag = vec4(color, 1.0);
	// gl_FragColor = frag;
	gl_FragColor = vec4((R + vec3(1.0, 1.0, 1.0)) / 2.0, 1.0);
}
