 # Lighting Toolkit v1.1.1

The first public version of a compilation of tools I usually use in my daily work.

<b>Lights</b>

  <b>· New</b>
  Creates a light previously selected on the lights combo.
  
  <b>· New from view</b>
  Creates a light from a camera, previously selected. Works fine with all kind of lights but I normally use it with <i>spotLights</i> or <i>areaLights</i>.
  
  <b>· New from objects</b>
  Creates a light on each object selected and creates a parent constraint to the light. In case you don't want it, you only have to delete it from the light.
  
  <b>· Isolate</b>
  Isolates the lights previously selected.
  
<b>Filters</b>

  <b>· New</b>
  Creates a filter previously selected on the filters combo into the light(s) selected.
  
  <b>· New from objects</b>
  Creates a filter on each object selected into the light(s) selected.
  
  <u>Note</u>: Normally, when you create a filter with Maya, only the <i>lightBlocker</i> is included into the defaultLightSet. If you create it into <b>Lighting Toolkit</b>, the filters are added into a new set named <i>defaultFilterSet</i> deleting itself from the <i>defaultLightSet</i>. This set, include all the filters, not just <i>lightBlocker</i>, to be more accessible. 
