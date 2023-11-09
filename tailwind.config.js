/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./snapcorrect/templates/**/*.html", "./snapcorrect/static/*.js", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {
      fontSize: {
        sm: "0.750rem",
        base: "1rem",
        xl: "1.333rem",
        "2xl": "1.777rem",
        "3xl": "2.369rem",
        "4xl": "3.158rem",
        "5xl": "4.210rem",
      },
      fontFamily: {
        heading: "Ubuntu",
        body: "Ubuntu",
      },
      fontWeight: {
        normal: "400",
        bold: "700",
      },
    },
  },
  plugins: [
    required("flowbite/plugin")
  ],
};
