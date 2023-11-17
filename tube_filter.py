# from tools import vtk_utils
import vtk_utils
import numpy as np
import vtkmodules.all as vtk
from vtkmodules.util import numpy_support


points = np.array([
    [1, 0, 0],
    [2, 0, 0],
    [3, 1, 0],
    [4, 1, 0],
    [2, 3, 4],
    [5, 3, 4],
])

vtk_array = numpy_support.numpy_to_vtk(points)
vtk_points = vtk.vtkPoints()
vtk_points.SetData(vtk_array)
  # points->InsertPoint(0, 1, 0, 0);
  # points->InsertPoint(1, 2, 0, 0);
  # points->InsertPoint(2, 3, 1, 0);
  # points->InsertPoint(3, 4, 1, 0);
  # points->InsertPoint(4, 5, 0, 0);
  # points->InsertPoint(5, 6, 0, 0);
# vtk.vtkPosp
spline = vtk.vtkParametricSpline()
spline.SetPoints(vtk_points)
  # // Fit a spline to the points.
  # vtkNew<vtkParametricSpline> spline;
  # spline->SetPoints(points);
functionSource =  vtk.vtkParametricFunctionSource()
functionSource.SetParametricFunction(spline)
functionSource.SetUResolution(10 * vtk_points.GetNumberOfPoints())
functionSource.Update()

# // Interpolate the scalars.
# double rad;
# vtkNew<vtkTupleInterpolator> interpolatedRadius;
# interpolatedRadius->SetInterpolationTypeToLinear();
# interpolatedRadius->SetNumberOfComponents(1);
# interpolatedRadius = vtk.vtkTupleInterpolator()

interpolatedRadius = vtk.vtkTupleInterpolator()
interpolatedRadius.SetInterpolationTypeToLinear()
interpolatedRadius.SetNumberOfComponents(1)
radius = [
    .2, .3, .35, .1, .2, 0.15
]
for i, rad in enumerate(radius):
    interpolatedRadius.AddTuple(i, [rad])
#
# rad = .2;
# interpolatedRadius->AddTuple(0, &rad);
# rad = .2;
# interpolatedRadius->AddTuple(1, &rad);
# rad = .2;
# interpolatedRadius->AddTuple(2, &rad);
# rad = .1;
# interpolatedRadius->AddTuple(3, &rad);
# rad = .1;
# interpolatedRadius->AddTuple(4, &rad);
# rad = .1;
# interpolatedRadius->AddTuple(5, &rad);

n = functionSource.GetOutput().GetNumberOfPoints()
# tubeRadius.
#   // Generate the radius scalars.
#   vtkNew<vtkDoubleArray> tubeRadius;
#   unsigned int n = functionSource->GetOutput()->GetNumberOfPoints();
#   tubeRadius->SetNumberOfTuples(n);
#   tubeRadius->SetName("TubeRadius");
tMin = interpolatedRadius.GetMinimumT();
tMax = interpolatedRadius.GetMaximumT();
#   double r;
radius_list = []
for i in range(n):
    t = (tMax - tMin) / (n - 1) * i + tMin
    ps = [0.]
    interpolatedRadius.InterpolateTuple(t, ps)
    radius_list.append(ps[0])
    # interpolatedRadius.InterpolateTuple(t)
radius_vtk = numpy_support.numpy_to_vtk(np.array(radius_list))
radius_vtk.SetName("TubeRadius")
  #
  # for (unsigned int i = 0; i < n; ++i)
  # {
  #   auto t = (tMax - tMin) / (n - 1) * i + tMin;
  #   interpolatedRadius->InterpolateTuple(t, &r);
  #   tubeRadius->SetTuple1(i, r);
  # }
  #
  # // Add the scalars to the polydata.
tubePolyData = functionSource.GetOutput();
tubePolyData.GetPointData().AddArray(radius_vtk);
tubePolyData.GetPointData().SetActiveScalars("TubeRadius");
  #
  # // Create the tubes.
tuber = vtk.vtkTubeFilter()
tuber.SetInputData(tubePolyData);
tuber.SetNumberOfSides(20);
tuber.SetVaryRadiusToVaryRadiusByAbsoluteScalar();
tuber.SetCapping(1)
tuber.Update()

res = tuber.GetOutput()
  #

vtk_utils.show_actors([
    vtk_utils.polydata2actor(res)
])
  # //--------------
  # // Setup actors and mappers.
  # vtkNew<vtkPolyDataMapper> lineMapper;
  # lineMapper->SetInputData(tubePolyData);
  # lineMapper->SetScalarRange(tubePolyData->GetScalarRange());
