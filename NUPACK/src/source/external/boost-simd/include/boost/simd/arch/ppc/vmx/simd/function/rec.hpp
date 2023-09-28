//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#ifndef BOOST_SIMD_ARCH_PPC_VMX_SIMD_FUNCTION_REC_HPP_INCLUDED
#define BOOST_SIMD_ARCH_PPC_VMX_SIMD_FUNCTION_REC_HPP_INCLUDED

#include <boost/simd/detail/overload.hpp>
#include <boost/simd/function/refine_rec.hpp>
#include <boost/simd/function/if_else.hpp>
#include <boost/simd/function/is_eqz.hpp>
#include <boost/simd/constant/inf.hpp>

#if !defined( BOOST_SIMD_NO_INFINITIES )
#include <boost/simd/constant/mzero.hpp>
#include <boost/simd/function/is_inf.hpp>
#endif

namespace boost { namespace simd { namespace ext
{
  namespace bd = boost::dispatch;
  namespace bs = boost::simd;

  BOOST_DISPATCH_OVERLOAD ( rec_
                          , (typename A0)
                          , bs::vmx_
                          , bs::pack_< bd::floating_<A0>, bs::vmx_>
                          )
  {
    BOOST_FORCEINLINE A0 operator()( const A0& a0) const BOOST_NOEXCEPT
    {
      A0 estimate = refine_rec(a0, raw_(rec)(a0));

      // fix rec(+/-0)
      estimate = if_else( is_eqz(a0)
                        , bitwise_or(a0, Inf<A0>())
                        , estimate
                        );

      // fix rec(+/-inf)
      #if !defined( BOOST_SIMD_NO_INFINITIES )
      estimate = if_else( is_inf(a0)
                        , bitwise_and(a0, Mzero<A0>())
                        , estimate
                        );
      #endif

      return estimate;
    }
  };

  BOOST_DISPATCH_OVERLOAD ( rec_
                          , (typename A0)
                          , bs::vmx_
                          , bs::raw_tag
                          , bs::pack_< bd::floating_<A0>, bs::vmx_>
                          )
  {
    BOOST_FORCEINLINE A0 operator()(bs::raw_tag const&, const A0& a0) const BOOST_NOEXCEPT
    {
      return vec_re( a0.storage() );
    }
  };
} } }

#endif
