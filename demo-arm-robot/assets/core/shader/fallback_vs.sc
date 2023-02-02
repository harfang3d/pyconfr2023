$input a_position, a_normal, a_texcoord0, a_texcoord1, a_tangent, a_bitangent, a_indices, a_weight
$output vWorldPos, vModelPos, vNormal, vModelNormal, vTexCoord0, vTexCoord1, vTangent, vBinormal, vLinearShadowCoord0, vLinearShadowCoord1, vLinearShadowCoord2, vLinearShadowCoord3, vSpotShadowCoord, vProjPos, vPrevProjPos

#include <forward_pipeline.sh>

mat3 normal_mat(mat4 m) {
#if BGFX_SHADER_LANGUAGE_GLSL
	vec3 u = normalize(vec3(m[0].x, m[1].x, m[2].x));
	vec3 v = normalize(vec3(m[0].y, m[1].y, m[2].y));
	vec3 w = normalize(vec3(m[0].z, m[1].z, m[2].z));
#else
	vec3 u = normalize(m[0].xyz);
	vec3 v = normalize(m[1].xyz);
	vec3 w = normalize(m[2].xyz);
#endif

	return mtxFromRows(u, v, w);
}

void main() {
	// position
	vec4 vtx = vec4(a_position, 1.0);

	vec4 world_pos = mul(u_model[0], vtx);

	// normal
	vec4 normal = vec4(a_normal * 2. - 1., 0.);
	vModelNormal = normalize(normal.xyz);
	vNormal = mul(normal_mat(u_model[0]), normal.xyz);

	vec4 tangent = vec4(a_tangent * 2.0 - 1.0, 0.0);
	vec4 binormal = vec4(a_bitangent * 2.0 - 1.0, 0.0);

	vTangent = mul(u_model[0], tangent).xyz;
	vBinormal = mul(u_model[0], binormal).xyz;

	//
	vWorldPos = world_pos.xyz;
    vModelPos = vtx.xyz;

	vTexCoord0 = a_texcoord0;
	vTexCoord1 = a_texcoord1;

	//
	vec4 proj_pos = mul(uViewProjUnjittered, world_pos);

	//
	gl_Position = mul(u_viewProj, world_pos);
}
