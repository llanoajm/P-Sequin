//==================================================================================================
/*!
  @file

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <boost/simd/function/insert.hpp>
#include <boost/simd/detail/unroll.hpp>
#include <boost/simd/pack.hpp>
#include <simd_test.hpp>
#include <array>

namespace bs = boost::simd;
namespace bd = boost::dispatch;

template<typename A, typename P, typename... N>
void f( brigand::list<N...> const&, A& a, P& p)
{
  using T = typename P::value_type;
  BOOST_SIMD_LOCAL_UNROLL( a[N::value] = T(N::value+1) );
  BOOST_SIMD_LOCAL_UNROLL( (bs::insert(p, N::value, T(N::value+1))) );
}

template <typename T, std::size_t N, typename Env>
void test_st(Env& $)
{
  bs::pack<T, N>  p;
  std::array<T,N> a;

  f( brigand::range<std::size_t, 0, N>(),a,p);

  bs::pack<T, N> ref(&a[0], &a[0] + N);
  STF_IEEE_EQUAL(ref, p);
}

STF_CASE_TPL("Check static insert on pack" , STF_NUMERIC_TYPES)
{
  static const std::size_t N = boost::simd::pack<T>::static_size;

  test_st<T, N>($);
  test_st<T, N/2>($);
  test_st<T, N*2>($);
}
