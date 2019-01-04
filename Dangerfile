# Sometimes it's a README fix, or something like that - which isn't relevant for
# including in a project's CHANGELOG for example
declared_trivial = github.pr_title.include? "#trivial"

# Greating
welcome_message.custom_words = <<-CUSTOM_WORDS
  Hi, @#{github.pr_author}!!
  Welcome to #{github.pr_json[:base][:repo][:full_name]}! Thanks so much for joining us.
CUSTOM_WORDS
welcome_message.greet

commit_lint.check

# Make it more obvious that a PR is a work in progress and shouldn't be merged yet
warn("PR is classed as Work in Progress") if github.pr_title.include? "[WIP]"

# Warn when there is a big PR
warn("Big PR") if git.lines_of_code > 500

# Mainly to encourage writing up some reasoning about the PR, rather than
# just leaving a title
if github.pr_body.length < 5
  fail "Please provide a summary in the Pull Request description"
end

# Let people say that this isn't worth a CHANGELOG entry in the PR if they choose
declared_trivial = (github.pr_title + github.pr_body).include?("#trivial") || !has_app_changes

# Formatting
pep8.lint(use_inline_comments=true)

todoist.message = "Please fix all TODOS"
todoist.warn_for_todos