# Android Code Challenge

Welcome to this coding challenge! The goal is to assess your ability to build a
structured, maintainable, and user-friendly Android application using Kotlin. Take this
as an opportunity to demonstrate not just your technical skills, but also your
problem-solving approach, attention to detail, and architectural decisions.

## The data

Fetch the document from:

```
https://aruana-lumiform.github.io/mobile-code-challenge-tools/code-challenge/challenge.json
```

The JSON follows this structure:

- It contains **items**, which can be either Pages, Sections, or Questions.
- **Pages** are the topmost elements and can contain Sections or Questions.
- **Sections** have a title and may contain nested Sections and Questions.
- **Questions** can be of type `text` or `image`.

## Task

Build a native Android app using Kotlin that:

1. Fetches the JSON from the endpoint above, simulating an API request.
2. Displays the JSON content in a visually structured way, clearly representing the
   hierarchy and relationships between items.

## Requirements

- Font sizes should reflect hierarchy:
  - Pages → largest font size
  - Sections → medium font size, decreasing for nested sections
  - Questions → smallest font size
- For text-based questions, display the text directly.
- For image-based questions:
  - Fetch and display the image in a reduced size.
  - Clicking the image should open a new screen displaying the full-sized image and its title.
- Implement offline support, ensuring the app can display previously fetched data.
  Do this using a relational database of your choice.

## Bonus (optional)

- Handle network failures gracefully, providing a fallback mechanism for poor connections.

## Additional instructions

- The app should be hosted in a public GitHub repository with a well-structured README
  containing clear setup instructions.
- A well-organized commit history is a plus, as it reflects good development practices.

Feel free to leverage any online resources, including AI tools. However, keep in mind
that your code quality, architecture, testing strategy, and ability to justify design
choices will be evaluated.

## Final words 🚀

This is your chance to showcase your expertise! Approach the challenge with creativity
and attention to detail. Most importantly, enjoy the process and build something you're
proud of! 💡🔥
