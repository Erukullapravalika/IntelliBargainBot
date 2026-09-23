import { Link } from "react-router-dom";

export default function Home() {
  return (
    <main className="bg-gray-950 text-white">

      {/* HERO SECTION */}
      <section className="hero-bg min-h-[85vh] flex items-center">
        <div className="container mx-auto px-6 text-center max-w-4xl">

          <h1 className="mt-4 text-5xl lg:text-6xl font-bold leading-tight">
            Shop Smarter. <br />
            Negotiate Better.
          </h1>

          <p className="mt-6 text-lg text-gray-300 max-w-2xl mx-auto">
            Discover premium products and unlock smarter deals through
            real-time price negotiation.
          </p>

          <div className="mt-10 flex justify-center">
            <Link
              to="/products"
              className="px-8 py-4 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-medium hover:scale-105 transition duration-300"
            >
              Explore Products
            </Link>
          </div>

        </div>
      </section>

      {/* FEATURES SECTION */}
      <section className="container mx-auto px-6 py-20">

        <div className="text-center mb-14">
          <h2 className="text-3xl font-semibold">
            Smarter Shopping Experience
          </h2>

          <p className="mt-3 text-gray-400">
            Personalized deals and seamless bargaining designed for modern online shopping.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">

          <div className="p-8 rounded-2xl bg-gray-900 border border-gray-800 hover:border-blue-500 transition duration-300">
            <h3 className="text-xl font-semibold">
              Smart Price Negotiation
            </h3>

            <p className="mt-3 text-gray-400">
              Negotiate product prices instantly through an interactive shopping assistant.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-gray-900 border border-gray-800 hover:border-blue-500 transition duration-300">
            <h3 className="text-xl font-semibold">
              Personalized Offers
            </h3>

            <p className="mt-3 text-gray-400">
              Enjoy tailored deals and better offers based on your shopping experience.
            </p>
          </div>

          <div className="p-8 rounded-2xl bg-gray-900 border border-gray-800 hover:border-blue-500 transition duration-300">
            <h3 className="text-xl font-semibold">
              Real-Time Deal Assistant
            </h3>

            <p className="mt-3 text-gray-400">
              Experience smooth and natural bargaining while shopping online.
            </p>
          </div>

        </div>
      </section>

    </main>
  );
}