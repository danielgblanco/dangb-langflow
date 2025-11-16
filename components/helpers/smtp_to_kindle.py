import smtplib
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from ebooklib import epub

from langflow.custom import Component
from langflow.io import MultilineInput, Output, SecretStrInput, StrInput
from langflow.schema import Message

class SmtpToKindle(Component):
    display_name = "SMTP to Kindle"
    description = "Emails HTML input as an epub file attachment to a specified Kindle address using SMTP."
    icon = "send"
    name = "SmtpToKindle"

    inputs = [
        StrInput(
            name="author",
            display_name="Author",
            info="The author used for the book metadata",
            tool_mode=True,
        ),
        StrInput(
            name="title",
            display_name="Title",
            info="The title of the file used for the book metadata",
            tool_mode=True,
        ),
        MultilineInput(
            name="content",
            display_name="Content (HTML)",
            info="A string containing the file content, which can include HTML for formatting.",
            tool_mode=True,
        ),
        SecretStrInput(
            name="kindle_email",
            display_name="Kindle Email",
            info="Your @kindle.com email address.",
        ),
        SecretStrInput(
            name="sender_email",
            display_name="Sender Email",
            info="Your verified email (must be the one approved for your Kindle account).",
        ),
        SecretStrInput(
            name="app_password",
            display_name="Password / Token",
            info="Your email account password or an app-specific token.",
        ),
        StrInput(
            name="smtp_server",
            display_name="SMTP Server",
            info="Your SMTP server. For ProtonMail, use `smtp.protonmail.ch`.",
            value="smtp.protonmail.ch",
        ),
        StrInput(
            name="smtp_port",
            display_name="SMTP Port",
            info="The port for your SMTP server. Use 587 for STARTTLS.",
            value="587",
        ),
    ]

    outputs = [
        Output(
            display_name="Status Message",
            name="status_message",
            method="send_file_to_kindle"
        )
    ]

    def _create_epub_file(self, title: str, author: str, file_content: str, epub_path: str):
        """Creates an EPUB file at the specified path using EbookLib."""
        book = epub.EpubBook()
        book.set_title(title)
        book.add_author(author)
        book.set_language("en")

        c1 = epub.EpubHtml(
            content=file_content,
            lang="en",
            media_type="application/xhtml+xml",
            title=title,
            file_name="chapter1.xhtml"
        )
        book.add_item(c1)
        book.spine = [c1]
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        epub.write_epub(epub_path, book)

    def _send_email(self, title: str, filename: str, attachment_data: bytes):
        """Constructs and sends an email with the EPUB attachment."""
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.kindle_email
        msg["Subject"] = title
        
        msg.attach(MIMEText("Document attached for Kindle.", "plain"))

        part = MIMEApplication(attachment_data, _subtype="octet-stream")
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)

        self.log(f"Attempting to connect to {self.smtp_server}:{self.smtp_port} and send '{filename}'")

        smtp_port = int(self.smtp_port)
        with smtplib.SMTP(self.smtp_server, smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.sendmail(self.sender_email, self.kindle_email, msg.as_string())

    def send_file_to_kindle(self) -> Message:
        title = self.title
        author = self.author
        file_content = self.content
        filename = f"{title}.epub"

        try:
            with tempfile.NamedTemporaryFile(suffix=".epub") as temp_epub:
                epub_path = temp_epub.name

                # 1. Create the EPUB file
                self._create_epub_file(title, author, file_content, epub_path)

                # 2. Read the created file data
                with open(epub_path, "rb") as f:
                    attachment_data = f.read()

                if not attachment_data:
                    raise ValueError("Created EPUB file is empty. Attachment failed.")

                # 3. Send the email
                self._send_email(title, filename, attachment_data)
            
            status = f"Successfully sent '{filename}' to {self.kindle_email}"
            self.status = status
            return Message(text=status)

        except Exception as e:
            error_message = f"Failed to send to Kindle: {str(e)}"
            self.status = error_message
            return Message(text=error_message)
