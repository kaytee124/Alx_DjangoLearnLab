"""
Forms for the bookshelf app

SECURITY NOTES:
- All forms use Django's built-in validation to sanitize inputs
- Custom clean methods provide additional validation layers
- XSS prevention through input sanitization
- SQL injection prevention through ORM usage (no raw queries)
"""
from django import forms
from .models import Book, Author


class BookForm(forms.ModelForm):
    """
    Form for creating/editing books with comprehensive validation
    
    SECURITY FEATURES:
    - Input validation: All fields validated before processing
    - XSS prevention: Strips dangerous characters (<, >)
    - Length limits: Prevents buffer overflow attacks
    - Required fields: Ensures data integrity
    - ORM integration: Uses parameterized queries (SQL injection prevention)
    """
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Enter the book title (max 100 characters)'
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=True,
        empty_label='Select an author',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author']
    
    def clean_title(self):
        """
        Validate and sanitize book title
        
        SECURITY:
        - Strips whitespace: Prevents padding attacks
        - Validates non-empty: Ensures data integrity
        - Blocks HTML tags: Prevents XSS attacks by blocking < and >
        - Returns sanitized data: Safe to use in templates
        """
        title = self.cleaned_data.get('title')
        if title:
            # SECURITY: Strip whitespace to prevent padding attacks
            title = title.strip()
            if not title:
                raise forms.ValidationError('Title cannot be empty or only whitespace.')
            # SECURITY: Block HTML tags to prevent XSS attacks
            # Note: Django templates auto-escape, but this adds defense-in-depth
            if '<' in title or '>' in title:
                raise forms.ValidationError('Title contains invalid characters.')
        return title
    
    def clean_author(self):
        """
        Validate author selection
        
        SECURITY:
        - Ensures author is selected: Prevents invalid data
        - Uses ModelChoiceField: Only allows valid Author objects (SQL injection prevention)
        - Validates against database: Ensures referential integrity
        """
        author = self.cleaned_data.get('author')
        if not author:
            raise forms.ValidationError('Please select an author.')
        # SECURITY: ModelChoiceField automatically validates against Author.objects
        # This ensures only valid, existing authors can be selected
        return author


class ExampleForm(forms.Form):
    """
    Example form demonstrating Django form usage
    
    This form serves as an example of how to create and use Django forms
    with proper validation and security measures.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
        help_text='Enter your full name (max 100 characters)'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        help_text='Enter a valid email address'
    )
    
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your message'}),
        help_text='Enter your message (required)'
    )
    
    def clean_name(self):
        """
        Validate and sanitize name field
        
        SECURITY:
        - Strips whitespace: Prevents padding attacks
        - Validates non-empty: Ensures data integrity
        - Blocks HTML tags: Prevents XSS attacks
        """
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if not name:
                raise forms.ValidationError('Name cannot be empty or only whitespace.')
            if '<' in name or '>' in name:
                raise forms.ValidationError('Name contains invalid characters.')
        return name
    
    def clean_message(self):
        """
        Validate message field
        
        SECURITY:
        - Strips whitespace: Prevents padding attacks
        - Validates non-empty: Ensures data integrity
        """
        message = self.cleaned_data.get('message')
        if message:
            message = message.strip()
            if not message:
                raise forms.ValidationError('Message cannot be empty or only whitespace.')
        return message
