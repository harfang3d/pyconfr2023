$input vWorldPos, vModelPos, vNormal, vModelNormal, vTangent, vBinormal, vTexCoord0, vTexCoord1, vLinearShadowCoord0, vLinearShadowCoord1, vLinearShadowCoord2, vLinearShadowCoord3, vSpotShadowCoord, vProjPos, vPrevProjPos

#include <forward_pipeline.sh>
#include <fresnel_equations.sh>

// Surface attributes
uniform vec4 uDiffuseColor;
uniform vec4 uSelfColor;
uniform vec4 uMatAttribute;

float remap(float value, float low1, float high1, float low2, float high2) {
	return low2 + (value - low1) * (high2 - low2) / (high1 - low1);
}

// Entry point of the forward pipeline shader
void main() {
	vec3 color = uDiffuseColor.xyz;

	vec3 view = mul(u_view, vec4(vWorldPos, 1.0)).xyz;
	vec3 P = vWorldPos; // fragment world pos
	vec3 V = normalize(GetT(u_invView) - P); // view vector
	vec3 N = sign(dot(V,vNormal)) * normalize(vNormal); // geometry normal
	vec3 R = reflect(-V, N); // view reflection vector around normal
	float NdotV = clamp(dot(N, V), 0.0, 1.0);
	
	// Fresnel values
	float fake_fresnel = pow(NdotV, 2.0) * 0.85; // remap(fake_fresnel, 0.0, 0.5, 1.0, 0.0);
	fake_fresnel = 1.0 - remap(fake_fresnel, 0.0, 0.5, 1.0, 0.0);
	color = vec3(fake_fresnel, fake_fresnel, fake_fresnel);
	color = clamp(color, 0.0, 1.0);
	color *= uDiffuseColor.xyz;

	// color = smoothstep(0.45, 0.65, color);

	color += uSelfColor.xyz;

	float top_light = clamp((N.y + 1.0) * 0.5, 0.0, 1.0);
	top_light = smoothstep(0.25, 0.65, top_light);
	color += color * top_light * 0.25;

	float specular = smoothstep(0.7, 0.75, R.y);
	color += vec3(1.0, 1.0, 1.0) * specular;

	gl_FragColor = vec4(color, uDiffuseColor.w);
}
