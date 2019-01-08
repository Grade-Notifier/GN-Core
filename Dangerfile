# Sometimes it's a README fix, or something like that - which isn't relevant for
# including in a project's CHANGELOG for example

has_app_changes = !git.modified_files.grep(/lib/).empty?
declared_trivial = github.pr_title.include? "#trivial"

# Greating
welcome_message.custom_words = <<-CUSTOM_WORDS
  Hi, @#{github.pr_author}!!
  Welcome to #{github.pr_json[:base][:repo][:full_name]}! Thanks so much for joining us.
CUSTOM_WORDS
welcome_message.greet

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
pep8.count_errors

# todoist.message = "Please fix all TODOS"
# todoist.warn_for_todos

if github.pr_title.include? "[WIP]"
    auto_label.wip=(github.pr_json["number"])
  else
    auto_label.remove("WIP")
    # If you want to delete label
    # auto_label.delete("WIP")
end


forgot_tests = git.modified_files.grep(%r{tests.py}).empty?
if forgot_tests and not declared_trivial
	warn("It appears that you forgot to add a Unit Test to the test file.\n Please add a test and upload the new version.\n The test file can currently be found at: ./src/tests/test/.py")
end

## Unit Tests
system("python3 ./src/tests/tests.py 2> log.txt")
unit_text = File.read("./log.txt")
if not unit_text.include?('OK')
	fail(unit_text)
else
	message("All Unit Test Passed! 🤟")
end






