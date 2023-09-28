//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <boost/simd/range/aligned_output_range.hpp>
#include <boost/simd/memory/allocator.hpp>
#include <boost/simd/pack.hpp>
#include <boost/simd/function/splat.hpp>
#include <boost/range/algorithm/generate.hpp>
#include <simd_test.hpp>
#include <vector>

STF_CASE_TPL("distance", STF_NUMERIC_TYPES)
{
  using boost::simd::aligned_output_range;
  using boost::simd::pack;

  std::vector<T,boost::simd::allocator<T>> data(pack<T>::static_size*3);
  std::vector<T,boost::simd::allocator<T,8>> data2(24);

  auto rng  = aligned_output_range(data);
  auto rng8 = aligned_output_range<8>(data2);

  STF_EQUAL( std::distance(std::begin(rng) , std::end(rng) ), 3 );
  STF_EQUAL( std::distance(std::begin(rng8), std::end(rng8)), 3 );
}

template<class T> struct generate
{
  generate(T v) : value(v) {}
  boost::simd::pack<T> operator()() const { return boost::simd::pack<T>(value++); }

  private:
  mutable T value;
};

STF_CASE_TPL("iteration", STF_NUMERIC_TYPES)
{
  using boost::simd::aligned_output_range;
  using boost::simd::pack;

  std::size_t ps = pack<T>::static_size;
  std::vector<T, boost::simd::allocator<T> >  ref (4*ps), data(4*ps);

  for(std::size_t i=0;i<data.size();i++)  data[i] = T(0);
  for(std::size_t i=0;i<ref.size();i++)   ref[i]  = T(i/pack<T>::static_size+1);

  auto simd_range = aligned_output_range(data);

  T k = 0;
  for(auto& e : simd_range) e = pack<T>(++k);

  STF_EQUAL( ref, data );
}
