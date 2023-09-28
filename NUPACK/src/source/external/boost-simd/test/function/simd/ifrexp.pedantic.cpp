//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <boost/simd/function/ifrexp.hpp>
#include <boost/simd/function/pedantic.hpp>
#include <boost/simd/detail/constant/minexponent.hpp>
#include <boost/simd/constant/halfeps.hpp>
#include <boost/simd/constant/valmax.hpp>
#include <boost/simd/pack.hpp>
#include <utility>

#include <simd_test.hpp>

namespace bs = boost::simd;
namespace bd = boost::dispatch;

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  using iT   = bd::as_integer_t<T>;
  using p_iT = bs::pack<iT, N>;
  using p_T  = bs::pack< T, N>;

  T a1[N], m[N];
  iT e[N];

  for(std::size_t i = 0; i < N; ++i)
  {
    a1[i] = (i%2) ? T(1+i) : -T(1+i);
    std::tie(m[i], e[i])   = bs::pedantic_(bs::ifrexp)(a1[i]);
  }

  p_T  in(&a1[0], &a1[0]+N);
  p_T  mm( &m[0],  &m[0]+N);
  p_iT ee( &e[0],  &e[0]+N);

  auto that = bs::pedantic_(bs::ifrexp)(in);

  STF_EQUAL(that.first, mm);
  STF_EQUAL(that.second, ee);
}

STF_CASE_TPL("Check basic behavior of pedantic(ifrexp) on pack" , STF_IEEE_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;
  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}

STF_CASE_TPL("Check behavior of pedantic_(ifrexp) on Zero", STF_IEEE_TYPES)
{
  using iT = bd::as_integer_t<T>;
  auto r = bs::pedantic_(bs::ifrexp)(bs::pack<T>(0));

  STF_EQUAL (r.first , bs::pack< T>(0));
  STF_EQUAL (r.second, bs::pack<iT>(0));
}

STF_CASE_TPL("Check behavior of pedantic_(ifrexp) on Valmax", STF_IEEE_TYPES)
{
  auto r = bs::pedantic_(bs::ifrexp)(bs::Valmax<bs::pack<T>>());

  STF_ULP_EQUAL (r.first , 1-bs::Halfeps<bs::pack<T>>(), 1);
  STF_EQUAL (r.second, bs::Limitexponent<bs::pack<T>>());
}

#ifndef BOOST_SIMD_NO_INVALID
#include <boost/simd/constant/nan.hpp>
STF_CASE_TPL("Check behavior of pedantic_(ifrexp) on NaN", STF_IEEE_TYPES)
{
  using iT = bd::as_integer_t<T>;
  auto r = bs::pedantic_(bs::ifrexp)(bs::Nan<bs::pack<T>>());

  STF_IEEE_EQUAL(r.first , bs::Nan<bs::pack<T>>());
  STF_EQUAL     (r.second, bs::pack<iT>(0));
}
#endif

#ifndef BOOST_SIMD_NO_INFINITIES
#include <boost/simd/constant/inf.hpp>
#include <boost/simd/constant/minf.hpp>

STF_CASE_TPL("Check behavior of pedantic_(ifrexp) on infinites", STF_IEEE_TYPES)
{
  using iT = bd::as_integer_t<T>;
  auto r = bs::pedantic_(bs::ifrexp)(bs::Inf<bs::pack<T>>());
  auto q = bs::pedantic_(bs::ifrexp)(bs::Minf<bs::pack<T>>());

  STF_IEEE_EQUAL(r.first , bs::Inf<bs::pack<T>>());
  STF_EQUAL     (r.second, bs::pack<iT>(0));

  STF_IEEE_EQUAL(q.first , bs::Minf<bs::pack<T>>());
  STF_EQUAL     (q.second, bs::pack<iT>(0));
}

#endif

#ifndef BOOST_SIMD_NO_DENORMALS
#include <boost/simd/detail/constant/minexponent.hpp>
#include <boost/simd/constant/mindenormal.hpp>

STF_CASE_TPL("Check behavior of pedantic_(ifrexp) on denormals", STF_IEEE_TYPES)
{
  auto r = bs::pedantic_(bs::ifrexp)(bs::Mindenormal<bs::pack<T>>());

  STF_ULP_EQUAL(r.first , bs::pack<T>(0.5), 1);
  STF_EQUAL     (r.second, bs::Minexponent<bs::pack<T>>()-bs::Nbmantissabits<bs::pack<T>>()+1);
}

#endif
