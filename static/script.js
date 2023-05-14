class Tag {
  constructor() {
    this.$tagRow = $("#tag-row");
    this.$tagForm = $("#tag-form");
    this.$tagInput = $("#tag-input");

    this.$tagForm.on("submit", this.handleTagSubmit.bind(this));
  }

  handleTagSubmit(evt) {
    evt.preventDefault();
    const tagName = this.$tagInput.val().toLowerCase();
    const $newCol = $("<div>").attr({ class: "col" });
    const $newTagBtn = $("<input>").attr({
      value: `${tagName}`,
      type: "checkbox",
      class: "btn-check",
      id: `tag-${tagName}`,
      autocomplete: "off",
      name: "tags",
      checked: true,
    });
    const $newTagLbl = $("<label>")
      .attr({
        for: `tag-${tagName}`,
        class: "btn btn-sm btn-outline-primary",
      })
      .text(`${tagName}`);
    $newCol.append($newTagBtn, $newTagLbl);
    this.$tagRow.append($newCol);
  }
}

tag = new Tag();
