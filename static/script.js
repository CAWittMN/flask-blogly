class Tag {
  constructor() {
    this.$tagContainer = $("#tag-container");
    this.$tagForm = $("#tag-field");
    this.$tagForm.on("submit", this.handleSubmit.bind(this));
  }

  handleSubmit(evt) {
    evt.preventDefault();
    const newTagName = this.$tagForm.val();
    $newTagPill = $("<input>");
    $newTagPill.attr({ value: `${newTagName}` });
  }
}
