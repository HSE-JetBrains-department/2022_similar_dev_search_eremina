# Code as Data. Developer similarity

# Project objectives
- Learn the basics of working with code as data
- Study the process of working with с git/GitHub API/programming languages classifier/code as AST
- Apply the knowlege in pratice to implement "Developer similarity" project  

# Steps of work
- Use git to extract useful information
    - Collect data from commits in public github repositories
    - Aggregate data by specific author name/email
- Extract information from source code
    - Classify programming languages using [enry](https://github.com/go-enry/go-enry)
    - Extract AST from code using [tree-sitter](https://github.com/tree-sitter/tree-sitter)
- Summarize data to create project
    - Prepare data
    - Create model
    - Choose quality metrics
    - Write tests
    - Configure CI
    - Build docker image

# Course grade
GRADE = (github_api * 0.15 + git * 0.25 + enry * 0.2 + tree_sitter * 0.25 + similar_dev_search * 0.15) * 8 + (tests + style_check + docker) * 2/3 \
Each item represents corresponding hometask
