module Problem3
where

import System.Time


--Method 1
isPrime :: Integer -> Bool
isPrime 2 = True
isPrime n =  not $ any (\x-> n  x == 0)  (2:[x | x<- [3 .. (floor ( sqrt $ fromIntegral n ))], odd x])



--Method 2
primes :: [Integer]
primes = sieve [2..]
  where
      sieve (p:xs) = p : sieve [x|x <- xs, x  p > 0]




--Method 3
divisors :: Integer -> [Integer]
divisors 1 = [1]
divisors x = 1:[ y | y <- [2..(x  2)], x  y == 0] ++ [x]

isPrime2 :: Integer -> Bool
isPrime2 x = divisors x == [1,x]




--Just to measure the time.
main :: IO ()
main = do
        startTime <- getClockTime
        print $ take 200000 [x| x<- [2 .. ], isPrime x] --201 seconds
--        print $ take 200000 [x| x<- [2 .. ], isPrime2 x] -- on the same machine, it didn't finish in 10 hours
--      print $ take 200000 primes -- on the same machine, it didn't finish in one hour.
        endTime   <- getClockTime
        print $ timeDiffToString $ diffClockTimes endTime startTime

