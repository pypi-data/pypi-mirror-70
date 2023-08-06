# Secure Equality Testing

`python3.8` package for secure equality testing, implementation of the EQT-1 protocol of [this paper](https://dl.acm.org/doi/10.1145/3230833.3230866)

### Example usage

With predetermined `a` and `b`


    from eqt.protocol import Protocol

    p = Protocol(a=12313, b=12312, kappa=40)
    p.start()
    print(p.decrypted_result)

    p = Protocol(a=12313, b=12313, kappa=40)
    p.start()
    print(p.decrypted_result)


Using `a` and `b` as input

    from eqt.main import main
    main()

To see timing results

    from eqt.timing import timing
    timing()