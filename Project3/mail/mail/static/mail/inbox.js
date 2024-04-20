document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const email_div = document.createElement('div');
      email_div.classList.add('border');

      if (email['read'] === true) { // If read, change background color to gray
        email_div.style.backgroundColor = 'gray';
      }

      const email_text_div = document.createElement('div');
      let h1 = document.createElement('h1');
      h1.innerHTML = 'Subject: ' + email['subject'];
      email_text_div.appendChild(h1);

      let h3_from = document.createElement('h3');
      h3_from.innerHTML = 'From: ' + email['sender'];
      email_text_div.appendChild(h3_from);

      let h3_to = document.createElement('h3');
      h3_to.innerHTML = 'To: ' + email['recipients'];
      email_text_div.appendChild(h3_to);

      let h4 = document.createElement('h4');
      h4.innerHTML = email['timestamp'];
      email_text_div.appendChild(h4);

      email_div.appendChild(email_text_div);

      email_div.addEventListener('click', function() {
        view_email(email);
      });

      const br = document.createElement('br');

      document.querySelector('#emails-view').append(email_div);
      document.querySelector('#emails-view').append(br);
    })

});

}

function view_email(email) {
  document.querySelector('#single-email-view').innerHTML = '';
  document.querySelector('#single-email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  fetch('/emails/' + email.id)
  .then(response => response.json())
  .then(email => {

    ////////////////////////////////////////////////////// - Creating Basic Elements

    const view_div = document.createElement('div');

    let h2_subject = document.createElement('h2');
    h2_subject.innerHTML = 'Subject: ' + email['subject'];
    view_div.appendChild(h2_subject);

    let h3_from = document.createElement('h3');
    h3_from.innerHTML = 'From: ' + email['sender'];
    view_div.appendChild(h3_from);

    let h3_to = document.createElement('h3');
    h3_to.innerHTML = 'To: ' + email['recipients'];
    view_div.appendChild(h3_to);

    let h4 = document.createElement('h4');
    h4.innerHTML = email['timestamp'];
    view_div.appendChild(h4);

    const br = document.createElement('br');
    view_div.appendChild(br);

    let body = document.createElement('p');
    body.innerHTML = email['body'];
    body.style.fontSize = '30px';
    view_div.appendChild(body);

    const br2 = document.createElement('br');
    view_div.appendChild(br2);

    ////////////////////////////////////////////////////// - Reply Button

    let reply_button = document.createElement('button');
    reply_button.innerHTML = 'Reply';
    reply_button.style.padding = '4px';

    reply_button.addEventListener('click', function() {
      compose_email();
      document.querySelector('#compose-recipients').value = email['sender']; // Pre-fill recipient

      if ( !(document.querySelector('#compose-subject').value.startsWith('RE: ')) ) { // Pre-fill subject
        document.querySelector('#compose-subject').value = 'RE: ' + email['subject'];
      }

      document.querySelector('#compose-body').value = 'On ' + email['timestamp'] + ' ' + email['sender'] + ' wrote: ' + '\n' + email['body'] + '\n\n';

    })

    view_div.append(reply_button);

    ////////////////////////////////////////////////////// - Archive/Unarchive Button

    if (email['archived'] === false) { // If not archived, make archive button
      let archive_button = document.createElement('button');
      archive_button.innerHTML = 'Archive';
      archive_button.style.borderRadius = '4px';
      archive_button.style.padding = '4px';

      archive_button.addEventListener('click', function() {
        fetch('/emails/' + email.id, { // Make read true
          method: 'PUT',
          body: JSON.stringify({
              archived: true
          })
        }).then(result => {
            load_mailbox('inbox');
          })
      })
      
      view_div.appendChild(archive_button);

    } else if (email['archived'] === true) { // If archived, make unarchive button
      let unarchive_button = document.createElement('button');
      unarchive_button.innerHTML = 'Unarchive';
      unarchive_button.style.borderRadius = '4px';
      unarchive_button.style.padding = '4px';

      unarchive_button.addEventListener('click', function() {
        fetch('/emails/' + email.id, { // Make read true
          method: 'PUT',
          body: JSON.stringify({
              archived: false
          })
        }).then(result => {
          load_mailbox('inbox');
        })
    })

      view_div.appendChild(unarchive_button);
    }

    //////////////////////////////////////////////////////

    document.querySelector('#single-email-view').append(view_div);
  })

  fetch('/emails/' + email.id, { // Make read true
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  }).then();

}

function send_email() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
        read: false, // set read and archived to false initially to prevent errors
        archived: false
    })
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox('sent');
    console.log(result);
  });

  return false;
}
