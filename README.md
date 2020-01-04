 # Lighting Toolkit v1.2.5

The first public version of a compilation of tools I usually use in daily work.

<b>Updates</b>

 · Light and filter listers added.

<b>Lights</b>

  <b>· Select Light Filters Button</b>
  Select the filters (aiLightBlocker) connected to a light previously selected.
  
<b>Filters</b>

  <b>· Select Filter Ligths Button</b>
  Select the lights connected to a filter (aiLightBlocker) previously selected.
  
<b>Tools/Lights</b>

  <b>· New</b>
  Creates a light previously selected on the lights combo.
  
  <b>· New from view</b>
  Creates a light from a camera, previously selected. Works fine with all kind of lights but normally, I use it with <i>spotLights</i> or <i>areaLights</i>.
  
  <b>· New from objects</b>
  Creates a light on each object previously selected and creates a parent constraint to the light. In case you don't want it, you only have to delete it from the light.
  
<b>Tools/Filters</b>

  <b>· New</b>
  Creates a filter previously selected on filters combo into the light(s) previously selected.
  
  <b>· New from objects</b>
  Creates a filter on each object selected into the light(s) previously selected.
  
  <u>Note</u>: In Maya, when you create a filter, only the <i>lightBlocker</i> is included into the defaultLightSet. If you create it into <b>Lighting Toolkit</b>, the filters are added into a new set named <i>defaultFilterSet</i> deleting itself from the <i>defaultLightSet</i>. This set include all the filters, not just <i>lightBlocker</i>, to be more accessible. 
