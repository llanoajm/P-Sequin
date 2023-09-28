//==================================================================================================
/*!

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <boost/simd/arch/common/detail/generic/horner.hpp>
#include <boost/simd/constant/mone.hpp>
#include <boost/simd/constant/mtwo.hpp>
#include <boost/simd/constant/one.hpp>
#include <boost/simd/constant/zero.hpp>
#include <boost/simd/constant/ten.hpp>
#include <boost/simd/function/horn.hpp>

#include <scalar_test.hpp>

using boost::simd::horner;
namespace bs =  boost::simd;

double f(const double & x)
{
  return horner<BOOST_SIMD_HORNER_COEFF_T(double, 4,
                                          (0x4010000000000000ll, //4
                                           0x4008000000000000ll, //3
                                           0x4000000000000000ll, //2
                                           0x3ff0000000000000ll  //1
                                          )
                                         )> (x);
}

float f(const float & x)
{
  return horner<BOOST_SIMD_HORNER_COEFF_T(float, 4,
                                          (0x40800000,  //4
                                           0x40400000,  //3
                                           0x40000000,  //2
                                           0x3f800000   //1
                                          )
                                         )> (x);
}

float g(const float & x)
{
  return bs::horn<float,
    0x3f800000ul, //1
    0x40000000ul, //2
    0x40400000ul, //3
    0x40800000ul  //4
 >(x);
}

float g(const double & x)
{
  return bs::horn<double,
    0x3ff0000000000000ull, //1
    0x4000000000000000ull, //2
    0x4008000000000000ull, //3
    0x4010000000000000ull  //4
 >(x);
}

STF_CASE_TPL( "Check horner behavior with floating", STF_IEEE_TYPES )
{
  namespace bs = boost::simd;
  using r_t = decltype(f(T()));
  STF_TYPE_IS(r_t, T);

  STF_EQUAL(f(bs::Zero<T>()), bs::One<r_t>());
  STF_EQUAL(f(bs::One<T>()),  bs::Ten<r_t>());
  STF_EQUAL(f(bs::Mone<T>()), bs::Mtwo<r_t>());
  STF_EQUAL(g(bs::Mone<T>()), bs::Mtwo<r_t>());
  STF_EQUAL(g(bs::One<T>()),  bs::Ten<r_t>());
  STF_EQUAL(g(bs::Mone<T>()), bs::Mtwo<r_t>());
}


