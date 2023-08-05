//
// Created by jtwok on 2020/3/8.
//

#ifndef SRC_PATH_H
#define SRC_PATH_H

#ifdef R_BUILD
#include <RcppEigen.h>
// [[Rcpp::depends(RcppEigen)]]
using namespace Eigen;
#else

#include <Eigen\Eigen>
#include "List.h"

#endif

#include "Data.h"
#include "Algorithm.h"
#include "Metric.h"

List sequential_path(Data &data, Algorithm *algorithm, Metric *metric,
                     Eigen::VectorXi sequence);

List gs_path(Data &data, Algorithm *algorithm, Metric *metric,
             int s_min, int s_max, int K_max, double epsilon);

#endif //SRC_PATH_H
