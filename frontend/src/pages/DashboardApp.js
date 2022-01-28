import React from 'react';
import {
  Stack,
  TextField,
  IconButton,
  InputAdornment,
  Button,
  Icon,
  Typography,
  Switch
} from '@mui/material';

import { useFormik, Form, FormikProvider } from 'formik';
import plusFill from '@iconify/icons-eva/plus-fill';

function DashboardApp() {
  const [checked, setChecked] = React.useState(true);
  const formik = useFormik({
    initialValues: {
      long_url: '',
      custom_url: '',
      api_key: '',
      custom: false
    }
    // validationSchema: LoginSchema,
    // onSubmit: () => {
    //   axios.get();
    //   navigate('/dashboard', { replace: true });
    // }
  });
  const { isSubmitting, handleSubmit, getFieldProps } = formik;
  return (
    <FormikProvider value={formik}>
      <Form autoComplete="off" noValidate onSubmit={() => {}}>
        <Stack spacing={3} style={{ margin: '3em', alignItems: 'center' }}>
          <Typography varient="h2"> Create a Short URL Today!</Typography>
          <TextField
            fullWidth
            label="original url"
            style={{ margin: '1em' }}
            {...getFieldProps('long_url')}
          />
          <Switch
            defaultChecked
            checked={checked}
            onClick={() => setChecked((checked) => !checked)}
            {...getFieldProps('custom')}
          />
          {checked && (
            <TextField
              fullWidth
              label="custom url"
              style={{ margin: '1em' }}
              {...getFieldProps('custom_url')}
            />
          )}
          <Button
            variant="contained"
            style={{ margin: '1em', width: '30%' }}
            to="#"
            startIcon={<Icon icon={plusFill} />}
          >
            Create Url
          </Button>
          <TextField
            fullWidth
            disabled
            style={{ margin: '1em' }}
            value="shorteneed url yaha aaye ga"
            // {...getFieldProps('short_url')}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={() => {}}
                    onMouseDown={() => {}}
                  >
                    <Icon icon={plusFill} />{' '}
                  </IconButton>
                </InputAdornment>
              )
            }}
          />
        </Stack>
      </Form>
    </FormikProvider>
  );
}

export default DashboardApp;
