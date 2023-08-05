#ifndef _GMLS_PYTHON_HPP_
#define _GMLS_PYTHON_HPP_

#include <Compadre_GMLS.hpp>
#include <Compadre_Evaluator.hpp>
#include <Compadre_PointCloudSearch.hpp>
#include <Compadre_KokkosParser.hpp>
#include <Kokkos_Core.hpp>
#include <Kokkos_Random.hpp>
#include <assert.h>
#ifdef COMPADRE_USE_MPI
    #include <mpi.h>
#endif

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

using namespace Compadre;
namespace py = pybind11;


class ParticleHelper {

private:

    Compadre::GMLS* gmls_object;
    typedef Kokkos::View<double**, Kokkos::HostSpace> double_2d_view_type;
    typedef Kokkos::View<int**, Kokkos::HostSpace> int_2d_view_type;
    typedef Kokkos::View<double*, Kokkos::HostSpace> double_1d_view_type;

    typedef nanoflann::KDTreeSingleIndexAdaptor<nanoflann::L2_Simple_Adaptor<double, Compadre::PointCloudSearch<double_2d_view_type> >, 
            Compadre::PointCloudSearch<double_2d_view_type>, 3> tree_type;
    std::shared_ptr<Compadre::PointCloudSearch<double_2d_view_type> > point_cloud_search;

    double_2d_view_type _source_coords;
    double_2d_view_type _target_coords;
    int_2d_view_type _neighbor_lists;
    double_1d_view_type _epsilon;

public:

    ParticleHelper(GMLS& gmls_instance) {
        gmls_object = &gmls_instance;
    }

    void setNeighbors(py::array_t<local_index_type> input) {
        py::buffer_info buf = input.request();

        if (buf.ndim != 2) {
            throw std::runtime_error("Number of dimensions must be two");
        }
        
        // create Kokkos View on host to copy into
        Kokkos::View<local_index_type**, Kokkos::HostSpace> neighbor_lists("neighbor lists", input.shape(0), input.shape(1));
        
        // overwrite existing data assuming a 2D layout
        auto data = input.unchecked<2>();
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,input.shape(0)), [=](int i) {
            for (int j = 0; j < input.shape(1); ++j)
            {
                neighbor_lists(i, j) = data(i, j);
            }
        });
        Kokkos::fence();
    
        // set values from Kokkos View
        gmls_object->setNeighborLists(neighbor_lists);
        _neighbor_lists = neighbor_lists;
    }

    py::array_t<local_index_type> getNeighbors() {
        compadre_assert_release((_neighbor_lists.extent(0)>0) && "getNeighborLists() called, but neighbor lists were never set.");

        auto dim_out_0 = _neighbor_lists.extent(0);
        auto dim_out_1 = _neighbor_lists.extent(1);

        auto result = py::array_t<local_index_type>(dim_out_0*dim_out_1);
        py::buffer_info buf_out = result.request();

        local_index_type *ptr = (local_index_type *) buf_out.ptr;
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,dim_out_0*dim_out_1), [&](int i) {
            ptr[i] = *(_neighbor_lists.data()+i);
        });
        Kokkos::fence();

        result.resize({dim_out_0,dim_out_1});
        return result;
    }

    void setSourceSites(py::array_t<double> input) {
        py::buffer_info buf = input.request();

        if (buf.ndim != 2) {
            throw std::runtime_error("Number of dimensions must be two");
        }

        if (gmls_object->getGlobalDimensions()!=input.shape(1)) {
            throw std::runtime_error("Second dimension must be the same as GMLS spatial dimension");
        }
        
        // create Kokkos View on host to copy into
        Kokkos::View<double**, Kokkos::HostSpace> source_coords("neighbor coordinates", input.shape(0), input.shape(1));
        
        // overwrite existing data assuming a 2D layout
        auto data = input.unchecked<2>();
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,input.shape(0)), [=](int i) {
            for (int j = 0; j < input.shape(1); ++j)
            {
                source_coords(i, j) = data(i, j);
            }
        });
        Kokkos::fence();
        
        // set values from Kokkos View
        gmls_object->setSourceSites(source_coords);
        _source_coords = source_coords;
    }

    py::array_t<double> getSourceSites() {
        compadre_assert_release((_source_coords.extent(0)>0) && "getSourceSites() called, but source sites were never set.");

        auto dim_out_0 = _source_coords.extent(0);
        auto dim_out_1 = _source_coords.extent(1);

        auto result = py::array_t<double>(dim_out_0*dim_out_1);
        py::buffer_info buf_out = result.request();

        double *ptr = (double *) buf_out.ptr;
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,dim_out_0*dim_out_1), [&](int i) {
            ptr[i] = *(_source_coords.data()+i);
        });
        Kokkos::fence();

        result.resize({dim_out_0,dim_out_1});
        return result;
    }

    void setTargetSites(py::array_t<double> input) {
        py::buffer_info buf = input.request();

        if (buf.ndim != 2) {
            throw std::runtime_error("Number of dimensions must be two");
        }

        if (gmls_object->getGlobalDimensions()!=input.shape(1)) {
            throw std::runtime_error("Second dimension must be the same as GMLS spatial dimension");
        }
        
        // create Kokkos View on host to copy into
        Kokkos::View<double**, Kokkos::HostSpace> target_coords("target coordinates", input.shape(0), input.shape(1));
        
        // overwrite existing data assuming a 2D layout
        auto data = input.unchecked<2>();
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,input.shape(0)), [=](int i) {
            for (int j = 0; j < input.shape(1); ++j)
            {
                target_coords(i, j) = data(i, j);
            }
        });
        Kokkos::fence();
        
        // set values from Kokkos View
        gmls_object->setTargetSites(target_coords);
        _target_coords = target_coords;
    }

    py::array_t<double> getTargetSites() {
        compadre_assert_release((_target_coords.extent(0)>0) && "getTargetSites() called, but target sites were never set.");

        auto dim_out_0 = _target_coords.extent(0);
        auto dim_out_1 = _target_coords.extent(1);

        auto result = py::array_t<double>(dim_out_0*dim_out_1);
        py::buffer_info buf_out = result.request();

        double *ptr = (double *) buf_out.ptr;
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,dim_out_0*dim_out_1), [&](int i) {
            ptr[i] = *(_target_coords.data()+i);
        });
        Kokkos::fence();

        result.resize({dim_out_0,dim_out_1});
        return result;
    }

    void setWindowSizes(py::array_t<double> input) {
        py::buffer_info buf = input.request();

        if (buf.ndim != 1) {
            throw std::runtime_error("Number of dimensions must be one");
        }
        
        // create Kokkos View on host to copy into
        Kokkos::View<double*, Kokkos::HostSpace> epsilon("h supports", input.shape(0));
        
        // overwrite existing data assuming a 2D layout
        auto data = input.unchecked<1>();
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,input.shape(0)), [=](int i) {
            epsilon(i) = data(i);
        });
        Kokkos::fence();
        
        // set values from Kokkos View
        gmls_object->setWindowSizes(epsilon);
        _epsilon = epsilon;
    }
 
    py::array_t<double> getWindowSizes() {
        if (_epsilon.extent(0)<=0) {
            throw std::runtime_error("getWindowSizes() called, but window sizes were never set.");
        }

        auto result = py::array_t<double>(_epsilon.extent(0));
        py::buffer_info buf = result.request();

        double *ptr = (double *) buf.ptr;
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,buf.shape[0]), [&](int i) {
            ptr[i] = _epsilon(i);
        });
        Kokkos::fence();

        return result;
    }

    void generateKDTree(py::array_t<double> input) {
        py::buffer_info buf = input.request();

        if (buf.ndim != 2) {
            throw std::runtime_error("Number of dimensions must be two");
        }

        if (gmls_object->getGlobalDimensions()!=input.shape(1)) {
            throw std::runtime_error("Second dimension must be the same as GMLS spatial dimension");
        }

        // create Kokkos View on host to copy into
        Kokkos::View<double**, Kokkos::HostSpace> source_coords("neighbor coordinates", input.shape(0), input.shape(1));
        
        // overwrite existing data assuming a 2D layout
        auto data = input.unchecked<2>();
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0, input.shape(0)), [=](int i) {
            for (int j = 0; j < input.shape(1); ++j)
            {
                source_coords(i, j) = data(i, j);
            }
        });
        point_cloud_search = std::shared_ptr<Compadre::PointCloudSearch<double_2d_view_type> >(new Compadre::PointCloudSearch<double_2d_view_type>(source_coords, gmls_object->getGlobalDimensions()));

        _source_coords = source_coords;
    }

    void generateNeighborListsFromKNNSearchAndSet(py::array_t<double> input, int poly_order, int dimension = 3, double epsilon_multiplier = 1.6, double maximum_neighbors_storage_multiplier = 1.0, double max_search_radius = 0.0) {

        int neighbors_needed = Compadre::GMLS::getNP(poly_order, dimension);

        py::buffer_info buf = input.request();

        if (buf.ndim != 2) {
            throw std::runtime_error("Number of dimensions must be two");
        }

        if (gmls_object->getGlobalDimensions()!=input.shape(1)) {
            throw std::runtime_error("Second dimension must be the same as GMLS spatial dimension");
        }
        
        // create Kokkos View on host to copy into
        Kokkos::View<double**, Kokkos::HostSpace> target_coords("target site coordinates", input.shape(0), input.shape(1));
        
        // overwrite existing data assuming a 2D layout
        auto data = input.unchecked<2>();
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,input.shape(0)), [=](int i) {
            for (int j = 0; j < input.shape(1); ++j)
            {
                target_coords(i, j) = data(i, j);
            }
        });

        // how many target sites
        int number_target_coords = target_coords.extent(0);

        // estimate storage requirements, but if storage_multiplier <= 0, then allocate as many entries as there are neighbors
        int estimated_upper_bound_number_neighbors = (maximum_neighbors_storage_multiplier > 0) ?
            (int)(maximum_neighbors_storage_multiplier*point_cloud_search->getEstimatedNumberNeighborsUpperBound(neighbors_needed, dimension, epsilon_multiplier))
            : _source_coords.extent(0)+1; // +1 for # of neighbors value
        
        // make neighbor list kokkos view
        int_2d_view_type neighbor_lists("neighbor lists", 
                number_target_coords, estimated_upper_bound_number_neighbors); // first column is # of neighbors
        
        // make epsilons kokkos view
        double_1d_view_type epsilon("h supports", number_target_coords);
        
        // call point_cloud_search using targets
        // use these neighbor lists and epsilons to set the gmls object
        point_cloud_search->generateNeighborListsFromKNNSearch(false /* not a dry run*/, target_coords, neighbor_lists, 
                epsilon, neighbors_needed, epsilon_multiplier, max_search_radius);

        Kokkos::fence();

        // set these views in the GMLS object
        gmls_object->setTargetSites(target_coords);
        gmls_object->setNeighborLists(neighbor_lists);
        gmls_object->setWindowSizes(epsilon);

        _target_coords = target_coords;
        _neighbor_lists = neighbor_lists;
        _epsilon = epsilon;

    }

    py::array_t<double> getPolynomialCoefficients(py::array_t<double> input) {
        py::buffer_info buf = input.request();

        // create Kokkos View on host to copy into
        Kokkos::View<double**, Kokkos::HostSpace> source_data("source data", input.shape(0), (buf.ndim>1) ? input.shape(1) : 1); 

        if (buf.ndim==1) {
            // overwrite existing data assuming a 2D layout
            auto data = input.unchecked<1>();
            Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0, input.shape(0)), [=](int i) {
                source_data(i, 0) = data(i);
            });
        } else if (buf.ndim>1) {
            // overwrite existing data assuming a 2D layout
            auto data = input.unchecked<2>();
            Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0, input.shape(0)), [=](int i) {
                for (int j = 0; j < input.shape(1); ++j)
                {
                    source_data(i, j) = data(i, j);
                }
            });
        }
        Kokkos::fence();


        // get polynomial coefficient size
        const int NP = gmls_object->getPolynomialCoefficientsSize();
        // get number of target sites
        const int NT = gmls_object->getNeighborLists().extent(0);

        Compadre::Evaluator gmls_evaluator(gmls_object);
        auto polynomial_coefficients = gmls_evaluator.applyFullPolynomialCoefficientsBasisToDataAllComponents<double**, Kokkos::HostSpace>
            (source_data);

        auto dim_out_0 = polynomial_coefficients.extent(0);
        auto dim_out_1 = polynomial_coefficients.extent(1);

        auto result = py::array_t<double>(dim_out_0*dim_out_1);
        py::buffer_info buf_out = result.request();

        double *ptr = (double *) buf_out.ptr;
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,dim_out_0*dim_out_1), [&](int i) {
            ptr[i] = *(polynomial_coefficients.data()+i);
        });
        Kokkos::fence();

        if (dim_out_1>1) {
            result.resize({dim_out_0,dim_out_1});
        }
        return result;
    }

    //PyObject* getAlphas0Tensor(int target_num, PyObject* pyObjectArray_neighborList) {
    //    // cast as a numpy array
    //    PyArrayObject *np_arr_neighborlist = reinterpret_cast<PyArrayObject*>(pyObjectArray_neighborList);

    //    int* loop_size = (int*)PyArray_GETPTR2(np_arr_neighborlist, target_num, 0);

    //    // copy data into Kokkos View
    //    // set dimensions
    //    npy_intp dims_out[1] = {*loop_size};

    //    // allocate memory for array 
    //    PyObject *pyObjectArray_out = PyArray_SimpleNew(1, dims_out, NPY_DOUBLE);
    //    if (!pyObjectArray_out) {
    //            printf("Out of memory.\n");
    //    }

    //    // recast as a numpy array and write assuming a 1D layout
    //    PyArrayObject *np_arr_out = reinterpret_cast<PyArrayObject*>(pyObjectArray_out);

    //    Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,*loop_size), [=](int i) {
    //        double alpha_evaluation = gmls_object->getAlpha0TensorTo0Tensor(Compadre::TargetOperation::ScalarPointEvaluation, target_num, i);
    //        double* val = (double*)PyArray_GETPTR1(np_arr_out, i);
    //        *val = alpha_evaluation;
    //    });

    //    // return the Python object
    //    return pyObjectArray_out;
    //}
 
    py::array_t<double> applyStencil(py::array_t<double> input, TargetOperation lro) {
        py::buffer_info buf = input.request();
 
        // create Kokkos View on host to copy into
        Kokkos::View<double**, Kokkos::HostSpace> source_data("source data", input.shape(0), (buf.ndim>1) ? input.shape(1) : 1); 

        if (buf.ndim==1) {
            // overwrite existing data assuming a 2D layout
            auto data = input.unchecked<1>();
            Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0, input.shape(0)), [=](int i) {
                source_data(i, 0) = data(i);
            });
        } else if (buf.ndim>1) {
            // overwrite existing data assuming a 2D layout
            auto data = input.unchecked<2>();
            Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0, input.shape(0)), [=](int i) {
                for (int j = 0; j < input.shape(1); ++j)
                {
                    source_data(i, j) = data(i, j);
                }
            });
        }
        Kokkos::fence();

        Compadre::Evaluator gmls_evaluator(gmls_object);
        if (lro==Compadre::TargetOperation::PartialYOfScalarPointEvaluation) {
            compadre_assert_release((gmls_object->getGlobalDimensions() > 1) && "Partial derivative w.r.t. y requested, but less than 2D problem.");
        } else if (lro==Compadre::TargetOperation::PartialZOfScalarPointEvaluation) {
            compadre_assert_release((gmls_object->getGlobalDimensions() > 2) && "Partial derivative w.r.t. z requested, but less than 3D problem.");
        }
        auto output_values = gmls_evaluator.applyAlphasToDataAllComponentsAllTargetSites<double**, Kokkos::HostSpace>
            (source_data, lro);

        auto dim_out_0 = output_values.extent(0);
        auto dim_out_1 = output_values.extent(1);

        auto result = py::array_t<double>(dim_out_0*dim_out_1);
        py::buffer_info buf_out = result.request();

        double *ptr = (double *) buf_out.ptr;
        Kokkos::parallel_for(Kokkos::RangePolicy<Kokkos::DefaultHostExecutionSpace>(0,dim_out_0*dim_out_1), [&](int i) {
            ptr[i] = *(output_values.data()+i);
        });
        Kokkos::fence();

        if (dim_out_1>1) {
            result.resize({dim_out_0,dim_out_1});
        }
        return result;
    }
};

template <typename... Args>
using overload_cast_ = pybind11::detail::overload_cast_impl<Args...>;

PYBIND11_MODULE(pycompadre, m) {
    m.doc() = R"pbdoc(
        Compadre Toolkit for Python
        -----------------------
        .. currentmodule:: pycompadre
        .. autosummary::
           :toctree: _generate

        GMLS
        KokkosParser
        ParticleHelper
        getNP
        getNN

    )pbdoc";

    // helper functions
    py::class_<ParticleHelper>(m, "ParticleHelper", R"pbdoc(
        Class to manage calling PointCloudSearch, moving data to/from Numpy arrays in Kokkos::Views,
        and applying GMLS solutions to multidimensional data arrays
    )pbdoc")
    .def(py::init<GMLS&>(),py::arg("gmls_instance"))
    .def("generateKDTree", &ParticleHelper::generateKDTree)
    .def("generateNeighborListsFromKNNSearchAndSet", &ParticleHelper::generateNeighborListsFromKNNSearchAndSet, 
            py::arg("target_sites"), py::arg("poly_order"), py::arg("dimension") = 3, py::arg("epsilon_multiplier") = 1.6, 
            py::arg("maximum_neighbors_storage_multiplier") = 1.0, py::arg("max_search_radius") = 0.0)
    .def("setNeighbors", &ParticleHelper::setNeighbors)
    .def("getNeighbors", &ParticleHelper::getNeighbors, py::return_value_policy::move)
    .def("setWindowSizes", &ParticleHelper::setWindowSizes)
    .def("getWindowSizes", &ParticleHelper::getWindowSizes, py::return_value_policy::move)
    .def("setSourceSites", &ParticleHelper::setSourceSites)
    .def("getSourceSites", &ParticleHelper::getSourceSites, py::return_value_policy::move)
    .def("setTargetSites", &ParticleHelper::setTargetSites)
    .def("getTargetSites", &ParticleHelper::getTargetSites, py::return_value_policy::move)
    .def("getPolynomialCoefficients", &ParticleHelper::getPolynomialCoefficients, py::return_value_policy::move)
    .def("applyStencil", &ParticleHelper::applyStencil,py::return_value_policy::move);
    

    py::class_<GMLS>(m, "GMLS")
    .def(py::init<int,int,std::string,std::string,std::string,int>(),
            py::arg("poly_order"),py::arg("dimension")=3,py::arg("dense_solver_type")="QR", 
            py::arg("problem_type")="STANDARD", py::arg("constraint_type")="NO_CONSTRAINT", 
            py::arg("curvature_poly_order")=2)
    .def(py::init<ReconstructionSpace,SamplingFunctional,int,int,std::string,std::string,std::string,int>(),
            py::arg("reconstruction_space"),py::arg("sampling_functional"),
            py::arg("poly_order"),py::arg("dimension")=3,py::arg("dense_solver_type")="QR", 
            py::arg("problem_type")="STANDARD", py::arg("constraint_type")="NO_CONSTRAINT", 
            py::arg("curvature_poly_order")=2)
    .def("setWeightingPower", &GMLS::setWeightingPower)
    .def("setWeightingType", overload_cast_<const std::string&>()(&GMLS::setWeightingType), "Set the weighting type.")
    //.def("setWeightingType", overload_cast_<WeightingType>()(&GMLS::setWeightingType), "Set the weighting type.")
    .def("addTargets", overload_cast_<TargetOperation>()(&GMLS::addTargets), "Add a target operation.")
    .def("addTargets", overload_cast_<std::vector<TargetOperation> >()(&GMLS::addTargets), "Add a list of target operations.")
    .def("generateAlphas", &GMLS::generateAlphas)
    .def("getNP", &GMLS::getNP, "Get size of basis.")
    .def("getNN", &GMLS::getNN, "Heuristic number of neighbors.");


    py::class_<KokkosParser>(m, "KokkosParser")
    .def(py::init<int,int,int,int,bool>());

    m.def("getNP", &GMLS::getNP, R"pbdoc(
        Get size of basis.
    )pbdoc");

    m.def("getNN", &GMLS::getNN, R"pbdoc(
        Heuristic number of neighbors.
    )pbdoc");

    py::class_<SamplingFunctional>(m, "SamplingFunctional");
    py::dict sampling_functional;
    sampling_functional["PointSample"] = PointSample;
    sampling_functional["VectorPointSample"] = VectorPointSample;
    sampling_functional["ManifoldVectorPointSample"] = ManifoldVectorPointSample;
    sampling_functional["StaggeredEdgeAnalyticGradientIntegralSample"] = StaggeredEdgeAnalyticGradientIntegralSample;
    sampling_functional["StaggeredEdgeIntegralSample"] = StaggeredEdgeIntegralSample;
    sampling_functional["VaryingManifoldVectorPointSample"] = VaryingManifoldVectorPointSample;
    sampling_functional["FaceNormalIntegralSample"] = FaceNormalIntegralSample;
    sampling_functional["FaceNormalPointSample"] = FaceNormalPointSample;
    sampling_functional["FaceTangentIntegralSample"] = FaceTangentIntegralSample;
    sampling_functional["FaceTangentPointSample"] = FaceTangentPointSample;
    sampling_functional["ScalarFaceAverageSample"] = ScalarFaceAverageSample;
    m.attr("SamplingFunctional") = sampling_functional;

    py::enum_<TargetOperation>(m, "TargetOperation")
    .value("ScalarPointEvaluation", TargetOperation::ScalarPointEvaluation)
    .value("VectorPointEvaluation", TargetOperation::VectorPointEvaluation)
    .value("LaplacianOfScalarPointEvaluation", TargetOperation::LaplacianOfScalarPointEvaluation)
    .value("VectorLaplacianPointEvaluation", TargetOperation::VectorLaplacianPointEvaluation)
    .value("GradientOfScalarPointEvaluation", TargetOperation::GradientOfScalarPointEvaluation)
    .value("GradientOfVectorPointEvaluation", TargetOperation::GradientOfVectorPointEvaluation)
    .value("DivergenceOfVectorPointEvaluation", TargetOperation::DivergenceOfVectorPointEvaluation)
    .value("CurlOfVectorPointEvaluation", TargetOperation::CurlOfVectorPointEvaluation)
    .value("CurlCurlOfVectorPointEvaluation", TargetOperation::CurlCurlOfVectorPointEvaluation)
    .value("PartialXOfScalarPointEvaluation", TargetOperation::PartialXOfScalarPointEvaluation)
    .value("PartialYOfScalarPointEvaluation", TargetOperation::PartialYOfScalarPointEvaluation)
    .value("PartialZOfScalarPointEvaluation", TargetOperation::PartialZOfScalarPointEvaluation)
    .value("ChainedStaggeredLaplacianOfScalarPointEvaluation", TargetOperation::ChainedStaggeredLaplacianOfScalarPointEvaluation)
    .value("GaussianCurvaturePointEvaluation", TargetOperation::GaussianCurvaturePointEvaluation)
    .value("ScalarFaceAverageEvaluation", TargetOperation::ScalarFaceAverageEvaluation)
    .export_values();


    py::enum_<ReconstructionSpace>(m, "ReconstructionSpace")
    .value("ScalarTaylorPolynomial", ReconstructionSpace::ScalarTaylorPolynomial)
    .value("VectorTaylorPolynomial", ReconstructionSpace::VectorTaylorPolynomial)
    .value("VectorOfScalarClonesTaylorPolynomial", ReconstructionSpace::VectorOfScalarClonesTaylorPolynomial)
    .value("DivergenceFreeVectorTaylorPolynomial", ReconstructionSpace::DivergenceFreeVectorTaylorPolynomial)
    .export_values();

#ifdef COMPADRE_SEMVER
    m.attr("__version__") = COMPADRE_SEMVER;
#else
    m.attr("__version__") = "dev";
#endif
}

#endif


